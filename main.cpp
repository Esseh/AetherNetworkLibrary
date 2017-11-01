#include<iostream>
#include<CPyWrapper.h>

int main(){
	std::string result;
	for(int i = 0; i < 1000000; i++){
	auto functionResult = CPy::Func("NetworkWrapper.wrapper","test",PyTuple_Pack(0),"uniqueCall");
	result = PyString_AsString(functionResult.result);
	}
	std::cout << result << std::endl;
}