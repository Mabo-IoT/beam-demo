# overview
python-beam-flink 
# issues
1. 可能需要本机有flink才行
2. `FlinkRunner`这个参数有问题，还是需要
   - ```./gradlew :runners:flink:1.8:job-server:runShadow -PflinkMasterUrl=localhost:8081D```开启jobservice
   - 然后输入`PortableRunner`参数
3. 只支持`flink1.8`，不支持1.9以上