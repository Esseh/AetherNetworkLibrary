compiler=x86_64-w64-mingw32-g++
python_include=C:\Python27\Python2764\include
cpywrapper_include=..\CPyWrapper
python_lib=C:\Python27\Python2764\libs
build-main: main.cpp
	$(compiler) -std=c++14 main.cpp CPyWrapper.a -I$(python_include) -I$(cpywrapper_include) -o main.exe