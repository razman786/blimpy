#include <string>
#include <iostream>
#include <fstream>
#include <memory>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

/*	To compile independent of setup.py:
c++ -O3 -Wall -shared -std=c++14 -fPIC -fopenmp `python3 -m pybind11 --includes` bound_reader.cpp -o bound_reader`python3-config --extension-suffix`
*/

namespace py = pybind11;

/* This is only a diagnostic function, to ensure that the binding was performed properly.
	Whenever I would want to expand the C++ modules to help with another python script,
	my first step in debugging would be to test the script's ability to use this adder.*/
int add(int i, int j) {
    return i + j;
}

py::array_t<float> read_sigproc_data(std::string filename, int data_index,
	int n_chan, int n_if, int n_int, int n_sel_chan,
	int chan_start_idx, int chan_stop_idx, unsigned char dtype_size)
{ 
	/* The Pybind approach to returning a Numpy array is somewhat byzantine;
		although 'container' is the return value, to modify its values we need
		to request a buffer and then a pointer to said buffer. */
	auto container = py::array_t<float>({n_int, n_if, n_sel_chan});
	py::buffer_info buffer = container.request();

	// fstream's file reader only accepts character pointers,
	// so we do not change this according to the data type
	char* index_ptr = (char*)buffer.ptr;	

	std::ifstream file (filename, std::ios::in|std::ios::binary);
	std::streampos curs = file.tellg();

	curs += data_index; // t_start (Python counterpart) not used here; could be a problem for functionality
	file.seekg(curs);

	// Arithmetic expressions in constants can be calculated and stored outside of the loop.
	// At the cost of some readability we avoid many redundant instructions.
	int jScale = n_sel_chan * dtype_size; // this is also the size of a contiguous batch of data to be read
	int iScale = n_if * jScale;
	int step = dtype_size * (n_chan - chan_stop_idx) + dtype_size * chan_start_idx;

	// The original Python code used relative indexing; I find the absolute integer cursor to be easier to track
	curs += dtype_size * chan_start_idx;
	file.seekg(curs);

	if (file.is_open()) {
		int offset = 0;
		/* Danny price pointed out that, since the vast majority of real-world data is stored on hard disks,
		it is unlikely that parallelizing the file reader will improve performance. I have left it in
		for the time being, because I have not yet evaluated the cost in overhead. If it is negligible,
		then the thread-spawning might at least be helpful for individuals with SSDs. */
		#pragma omp parallel for
		for (int i = 0; i < n_int; i++)
			/* There is room for loop unrolling here, but I leave that to those with more experience with
			the typical dimensions of data arrays. */
			for (int j = 0; j < n_if; j++) {
				offset = i * iScale + j * jScale;
				file.read(index_ptr + offset, jScale);				
				curs += step;
				file.seekg(curs);
			}
		file.close();
	}
	else {
		// Ideally this would be a formal error
		std::cout << "There was an error and the file could not be opened";
	}

	return container;
}


PYBIND11_MODULE(blimpy_read_module, m) {
	m.doc() = "Read binary file using pybind11";
	m.def("add", &add, "Adds two numbers (diagnostic function)");
	m.def("read_sigproc_data", &read_sigproc_data, 
    R"pbdoc(File Reader (formally of type float32, but in practice should be castable to any desiderata) )pbdoc",
    py::arg("filename"), 
    py::arg("data_index"), 
    py::arg("n_chan"), 
    py::arg("n_if"), 
    py::arg("n_int"), 
    py::arg("n_sel_chan"), 
    py::arg("chan_start_idx"), 
    py::arg("chan_stop_idx"), 
    py::arg("dtype_size")
    );
}
