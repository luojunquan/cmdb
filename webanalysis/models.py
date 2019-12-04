from django.db import models, connection


# Create your models here.

class AccessLogFile(models.Model):
    name = models.CharField(max_length=128,null=False,default='')
    path = models.CharField(max_length=1024,null=False,default='')
    created_time = models.DateTimeField(auto_now_add=True)
    #逻辑删除，默认0为不删除
    status = models.IntegerField(default=0)

#日志信息字段
class AccessLog(models.Model):
    file_id = models.IntegerField(default=0,null=False)
    #主机名
    hostname = models.CharField(max_length=526,null=True)
    #日志记录时间
    log_recording = models.DateTimeField(null=True)
    #缓存服务器IP地址
    cache_server = models.CharField(max_length=128,null=True)
    #发起请求的用户的源IP地址
    user_ip = models.CharField(max_length=128,null=True)
    #用户请求IP地址
    user_request_ip = models.CharField(max_length=128,null=True)
    #HTTP请求的Method字段内容
    http_methond = models.CharField(max_length=128,null=True)
    #HTTP请求的Host字段内容
    http_request_host = models.CharField(max_length=128,null=True)
    #HTTP请求的Uri字段内容
    http_url = models.CharField(max_length=5090,null=True)
    #缓存设备向用户返回的HTTP应答的Status-code字段内容
    http_status_code = models.IntegerField(default=0,null=True)
    #程序为用户提供服务的端口号,缓存服务器端口
    cache_server_port = models.IntegerField(null=True)
    #本次请求缓存向用户吐出的流量
    cache_to_user_flow = models.IntegerField(null=True)
    #回源IP
    back_to_source_ip = models.CharField(max_length=128,null=True)

    #去数据库进行http_status_code进行比对和查询
    @classmethod
    def dist_status_code(cls,file_id):
        cursor = connection.cursor()
        cursor.execute(
            '''
            select http_status_code,count(*) from webanalysis_accesslog 
            where file_id=%s group by http_status_code;
            ''',(file_id,))
        rt = cursor.fetchall()
        legend = []
        series = []
        for line in rt:
            legend.append(str(line[0]))
            series.append({"name":str(line[0]),"value":line[1]})
        return legend,series

    @classmethod
    def trend_visit(cls,file_id):
        cursor = connection.cursor()
        sql = 'select date_format(log_recording , "%%y-%%m-%%d %%h:%%i:%%s") as log_minute,count(*) as cnt from webanalysis_accesslog where file_id=%s group by log_minute'
        cursor.execute(sql,(file_id,))
        rt = cursor.fetchall()
        xAxis = []
        series = []
        for line in rt:
            xAxis.append(line[0])
            series.append(line[1])
        return xAxis, series

    @classmethod
    def request_user_ip(cls,file_id):
        cursor = connection.cursor()
        sql = 'select user_ip,count(*) from webanalysis_accesslog where file_id=%s group by user_ip;'
        cursor.execute(sql, (file_id,))
        rt = cursor.fetchall()
        xAxis = []
        series = []
        for line in rt:
            xAxis.append(line[0])
            series.append(line[1])
        return xAxis, series

    @classmethod
    def http_request_user_host(cls,file_id):
        cursor = connection.cursor()
        #sql = 'select http_request_host,count(*) as cnt from webanalysis_accesslog where file_id=%s group by http_request_host;'
        # sql = 'select user_ip,count(*) as cnt,sum(cache_to_user_flow) as sum_flow from webanalysis_accesslog where file_id=%s group by user_ip order by sum_flow desc limit 15;'
        #将sql查询出的数据进行拍寻，然后将数据进行添加行号
        #同一个IP多次请求缓存向用户吐出的流量
        sql = 'select @rank:=@rank+1 AS rank,web.* from (select web.user_ip,sum(web.cache_to_user_flow) as sum_flow from webanalysis_accesslog web where web.file_id=%s group by web.user_ip order by sum_flow desc) web,(select (@rank:=0) ) web_rank group by rank;'
        cursor.execute(sql, (file_id,))
        rt = cursor.fetchall()
        yAxis = []
        series = []
        for line in rt:
            #取出行号为前15的值
            if line[0] <= 15:
                yAxis.append(line[1])
                series.append(line[2])
        return yAxis, series