# genGarbageCode

genCppCode.py 随机生成c++垃圾代码  
```
> python .\genCppCode.py -h
usage: genCppCode.py [-h] [-p PREFIX] [-c CLASSNUM] [-m MEMBER] [-s STATIC]

options:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        prefix of class name
  -c CLASSNUM, --classnum CLASSNUM
                        number of cpp class file
  -m MEMBER, --member MEMBER
                        max number of member function in one class file
  -s STATIC, --static STATIC
                        max number of static function in one class file
```
默认生成20个包含头文件在内的C++类，类名前缀默认为OBFU，每个类默认最多10个类成员函数，最多2个类静态成员函数