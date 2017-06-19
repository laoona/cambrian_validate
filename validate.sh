#! /bin/bash
y=`date '+%Y'`
m=`date '+%m'`
M=`date '+%m'`
d=`date '+%d'`
D=`date '+%d'`
# 注释月日前导0
# m=${m/#0/}
# d=${d/#0/}

ymd=${y}-${m}-${d}

base_path=$(cd `dirname $0`; pwd);
path=${base_path}

txt="${path}/urls.txt"
validate_script="${path}/jsonld-validator/tool.py"
flag="mip链接校验通过 canonical标签校验通过 jsonld数据校验通过"

succ_n=0
fail_n=0

> ${path}/log.${ymd}.txt
> ${path}/urls.success.txt
> ${path}/urls.fail.txt

validateMain() {

    url=$1
    res=`/usr/bin/python ${validate_script} 1 ${url}`

    if [ "${#flag}" == "${#res}" ]
    then
        succ_n=`expr ${succ_n} + 1`

        echo  -e "\033[32m success\033[0m url[${url}]"
        echo "${ymd} ${url}" >> ${path}/urls.success.txt
        echo "success url[${url}]" >> ${path}/log.${ymd}.txt
        echo "time[${ymd}] success url[${url}]" >> ${path}/log.txt
    else    
        fail_n=`expr ${fail_n} + 1`

        echo "${ymd} ${url}" >> ${path}/urls.fail.txt
        echo -e "\033[31m fail\033[0m url[${url}] mesg[\033[31m${res}\033[0m]"
        echo "fail url[${url}] mesg[${res}]" >> ${path}/log.${ymd}.txt
        echo "time[${ymd}] fail url[${url}] mesg[${res}]" >> ${path}/log.txt
    fi

}

# echo "请输入校验类型(id|txt):"
# read type

type=$1

if [ "${type}" == "id" ]
then
    echo "请输入开始文章的id:"
    read id

    echo "请输入结束文章的id:"
    read id_end

    while [[ ${id} -le ${id_end} ]];
    do
        url="https://m.fh21.com.cn/news/mip/${id}.html"
        validateMain ${url}
        let "id++"
    done
else
    for url in `cat ${txt}`
    do
        validateMain ${url}
    done
fi

echo "[${succ_n}个校验通过] [${fail_n}个校验失败]"

