#include<iostream>
#include"json/json.hpp"
#include<CPyWrapper.h>
using json = nlohmann::json;

json callWrapperFunc(std::string str,std::string func);
json cppPortInterfaceWrapper(std::string str);
json cppHTTPInterfaceWrapper(std::string str);

int main(){
	json portOpener = {
		{"instruction","open"},
		{"protocol","UDP"},
		{"category","chat"},
		{"portNumber",4000}
	};
	json portSender = {
		{"instruction","put"},
		{"protocol","UDP"},
		{"portNumber",4000},
		{"ipAddress","127.0.0.1"},
		{"message","test message"}
	};
	json portReader = {
		{"instruction","get"},
		{"protocol","UDP"},
		{"category","chat"}
	};
	std::string inp1 = portOpener.dump();
	std::string inp2 = portSender.dump();
	std::string inp3 = portReader.dump();
	cppPortInterfaceWrapper(inp1);
	cppPortInterfaceWrapper(inp2);
	auto res = cppPortInterfaceWrapper(inp3);
	std::string result = res.dump();
	std::cout << result << std::endl;
}

json callWrapperFunc(std::string str,std::string func){
	auto functionResult = CPy::Func("NetworkWrapper.wrapper",func.c_str(),PyTuple_Pack(1,PyString_FromString(str.c_str())),"networkCall");
	std::string error = PyString_AsString(functionResult.error);
	std::string result = PyString_AsString(functionResult.result);
	std::cout << result << std::endl;
	if(error != ""){
		throw error;
	}
	if(result == "{}")
	return json::parse(result);	
}
json cppPortInterfaceWrapper(std::string str){
	return callWrapperFunc(str,"cppPortInterface");
}
json cppHTTPInterfaceWrapper(std::string str){
	return callWrapperFunc(str,"cppHTTPInterface");
}