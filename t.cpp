#include<iostream>
using namespace std;

int main(){
	std::string str = " {\"content\":\"hoi\"} ";
	json JSONexample = json::parse(str);
	cout << (JSONexample["content"]) << endl;
}