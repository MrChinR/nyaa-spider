# nyaa-spider
注意！！！
nyaa网站只有100页，sukebei只有50页，超过的页数将无法爬取。

 nyaa和sukebei的种子爬虫，通过一定的算法判断种子是否值得下载（是否是黑车），
爬取后的数据会存到同目录下的Excel文档中方便查阅。

大量爬取种子，多线程爬取时注意线程数不要过大，防止服务器403，
爬取种子可选择是否略过小于1g的种子文件。

是否为黑车的判断机制为：
U:上传数
D:下载数
F:完成数
DE:上传日期与爬种时相差的天数（例如今天是26号，23号的DE就是3）

结果=（F-U-D）/DE*（D/U）
数值越大越不是黑车…


以下为自动翻译（The following is automatic translation）
Attention!!!!!!
Nyaa site only 100 pages, sukebei only 50 pages, more than the number of pages will not be able to crawl.
Nyaa and sukebei seed crawler, through a certain algorithm to judge whether the seed is worth to download (whether black car), crawl the data will be endures with convenient access to Excel document in the directory.
A large number of crawl seeds, multi-threaded climb take note that the number of threads do not too big, to prevent the server 403, crawl seeds can choose whether to skip is less than 1 g seed file.
Whether for targeted judgment mechanism is: U: upload number D: download number F: complete count DE: upload date and climb a difference of the number of days (today is 26, for example, 23 DE is 3)
Results = (F - U - D)/DE * (D/U) numerical bigger is not a black car...
