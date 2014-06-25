$(function(){
    var xmlHttp = false;
    diff = null

    //获取服务器时间
    try {
        xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
        try {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch (e2) {
            xmlHttp = false;
        }
    }

    if(!xmlHttp && typeof XMLHttpRequest != 'undefined') {
        xmlHttp = new XMLHttpRequest();
    }

    //xmlHttp.open("GET","", false);
    xmlHttp.open("GET", "",  true);
    xmlHttp.setRequestHeader("Range", "bytes=-1");
    xmlHttp.send(null);
    xmlHttp.onreadystatechange = function(){
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status ==200){
                diff=new Date(xmlHttp.getResponseHeader("Date")).getTime()-new Date().getTime();
                clock();
            }
        }
    }
})

function clock()
{
    var x,h,m,s,n,xingqi,y,mon,d;
    var x = new Date(new Date().getTime()+diff);
    y = x.getYear()+1900;
    if (y>3000) y-=1900;
    mon = x.getMonth()+1;
    d = x.getDate();
    xingqi = x.getDay();
    h=x.getHours();
    m=x.getMinutes();
    s=x.getSeconds();

    n=y+"-"+mon+"-"+d+" "+(h>=10?h:"0"+h)+":"+(m>=10?m:"0"+m)+":"+(s>=10?s:"0"+s);
    //alert(n);
    document.getElementById('nowdate').innerHTML=n;
    setTimeout("clock()",1000);
} 

