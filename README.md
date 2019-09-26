# overview
python-beam-flink 
# issues
1. 可能需要本机有flink才行
2. `FlinkRunner`这个参数有问题，还是需要
   - ```./gradlew :runners:flink:1.8:job-server:runShadow -PflinkMasterUrl=localhost:8081```开启jobservice
   - 然后输入`PortableRunner`参数
3. 只支持`flink1.8`，不支持1.9以上
4. ```python -m apache_beam.examples.wordcount --input /home/heathkang/Projects/Proj-mv/Beam/beam-demo/test.txt --output /home/heathkang/Projects/Proj-mv/Beam/beam-demo/handle.txt --runner PortableRunner --environment_type=LOOPBACK --job_endpoint=localhost:8099``` is failed
5. ```python -m apache_beam.examples.wordcount --input /home/heathkang/Projects/Proj-mv/Beam/beam-demo/test.txt --output /home/heathkang/Projects/Proj-mv/Beam/beam-demo/handle.txt --runner FlinkRunner --environment_type=LOOPBACK --experiments=beam_fn_api --flink_master_url=localhost:8081``` is good **must have --experiments=beam_fn_api** 

# Program-model
`Pipline` ： `PCollection` => `Transform` => `PCollection` => `Transform`...
## pipline
整体数据流，从input 到 output
## PCollection
内部的data,可以是unbound或bound
### unbound
对于unbound数据，一般用window来进行数据的切割
#### window
- fixed window: 固定时间段的window,比如5分钟一个
- sliding window：有些重合的window,比如每10s一个，每个5分钟
- session window：

#### trigger
一些触发条件

## Transform
- ParDo: 类似于map
  - 可通过`beam.DoFn`来自定义ParDo操作
- GroupByKey： same key , different value ; collect
  - "cat,1, cat, 2,  dog:3" => "cat, [1,2], dog, [3]"
- CoGroupByKey:same key, different attribute;collect
  - ```
    emails_list = [
        ('amy', 'amy@example.com'),
        ('carl', 'carl@example.com'),
        ('julia', 'julia@example.com'),
        ('carl', 'carl@email.com'),
    ]
    phones_list = [
        ('amy', '111-222-3333'),
        ('james', '222-333-4444'),
        ('amy', '333-444-5555'),
        ('carl', '444-555-6666'),
    ]
    ``` 
  -  
 ``` 
   [
    ('amy', {
        'emails': ['amy@example.com'],
        'phones': ['111-222-3333', '333-444-5555']}),
    ('carl', {
        'emails': ['carl@email.com', 'carl@example.com'],
        'phones': ['444-555-6666']}),
    ('james', {
        'emails': [],
        'phones': ['222-333-4444']}),
    ('julia', {
        'emails': ['julia@example.com'],
        'phones': []}),
  ]
  ```
- Combine: 类似reduce,将data集合起来，比如add 累加
- Flatten： 将类型相同的几个data集合,merge到一个集合里
- Partition： 类似split,将data集合按func分割为不同集合

## metric
beam提供metric来查看当前计算的state

## nextsteps
1. 测试一下kafka的数据，看能否行的通
