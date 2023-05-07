#generate ARMA(2,1)
library("TSA")
library("ggplot2")
simu=arima.sim(n=300, list(ar = c(0.8, -0.5), ma = c(-0.4)))
simu=round(simu, digits = 3)
plot(simu)
acf(simu)
pacf(simu)
eacf(simu)
# write.csv(x=simu, file="D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/simulation.csv",col.names = FALSE,row.names = FALSE)

#Camouflage Data
data_camouflage1=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/camouflage data 1.csv',header = FALSE)
data_camouflage2=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/camouflage data 2.csv',header = FALSE)

#load original data
data_original1=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 1.csv',header = FALSE)
data_original2=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 2.csv',header = FALSE)
data_original3=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 3.csv',header = FALSE)
data_original4=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 4.csv',header = FALSE)
data_original5=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 5.csv',header = FALSE)
data_original6=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 6.csv',header = FALSE)
data_original7=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 7.csv',header = FALSE)
data_original8=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 8.csv',header = FALSE)
data_original9=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 9.csv',header = FALSE)
data_original10=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data 10.csv',header = FALSE)


#combine original data together
yValue1 <- data_original1[[1]]
yValue2 <- data_original2[[1]]
yValue3 <- data_original3[[1]]
yValue4 <- data_original4[[1]]
yValue5 <- data_original5[[1]]
yValue6 <- data_original6[[1]]
yValue7 <- data_original7[[1]]
yValue8 <- data_original8[[1]]
yValue9 <- data_original9[[1]]
yValue10 <- data_original10[[1]]

xValue1 <- 1:100
xValue_ori=1:10

y_original=c(yValue1,yValue2,yValue3,yValue4,yValue5,yValue6,yValue7,yValue8,yValue9,yValue10)

data_original_1window=data.frame(xValue_ori,yValue1)
data_original=data.frame(xValue1,y_original)

#combine camouflage data
xValue_cam=1:52

xValue2 <- 1:104
yValue_cam1 <- data_camouflage1[[1]]*(-0.5)-0.5
yValue_cam2 <- data_camouflage2[[1]]*(-0.5)-0.5
y_cam=c(yValue_cam1,yValue_cam2)

data_camouflage_1window=data.frame(xValue_cam,yValue_cam1)
data_camouflage=data.frame(xValue2,y_cam)

window_size=c(0,20,40,60,80,100)
window_size2=c(0,104)

#1 window original data
ggplot()+geom_line(data = data_original_1window,aes(x=xValue_ori,y=yValue1,color='yValue1'))+
  geom_point(data = data_original_1window,aes(x=xValue_ori,y=yValue1))+
  theme(axis.text=element_text(size=16, face="bold"),
        axis.title=element_text(size=14,face="bold"))+
  scale_x_continuous("Time", labels = as.character(xValue_ori), breaks = xValue_ori)


#1 window camouflage data
ggplot()+geom_line(data = data_camouflage_1window,aes(x=xValue_cam,y=yValue_cam1,color='yValue2'),color='blue')+
  geom_point(data = data_camouflage_1window,aes(x=xValue_cam,y=yValue_cam1))+
  theme(axis.text=element_text(size=16, face="bold"),
        axis.title=element_text(size=14,face="bold"))+
  scale_x_continuous("Time", labels = as.character(window_size), breaks = window_size)


#10 window original data
ggplot()+geom_line(data = data_original,aes(x=xValue1,y=y_original,color='original data'))+
  geom_point(data = data_original,aes(x=xValue1,y=y_original))+
  scale_x_continuous("Time", labels = as.character(window_size), breaks = window_size)+
  theme(axis.text=element_text(size=16, face="bold"),
        axis.title=element_text(size=14,face="bold"))

#2 window camouflage data
ggplot()+geom_line(data = data_camouflage,aes(x=xValue2,y=y_cam,color='yValue2'),color='blue')+
  geom_point(data = data_camouflage,aes(x=xValue2,y=y_cam))+
  theme(axis.text=element_text(size=16, face="bold"),
        axis.title=element_text(size=14,face="bold")) +
  scale_x_continuous("Time", labels = as.character(window_size), breaks = window_size)

# ggplot()+
#   geom_line(data = data_camouflage1,aes(x=xValue1,y=yValue_cam1,color='camouflage1'))+
#   geom_line(data = data_camouflage2,aes(x=xValue1,y=yValue_cam2,color='camouflage2'))+
#   geom_line(data = data_camouflage3,aes(x=xValue1,y=yValue_cam3,color='camouflage3'))+
#   geom_line(data = data_camouflage4,aes(x=xValue1,y=yValue_cam4,color='camouflage4'))+
#   geom_line(data = data_camouflage5,aes(x=xValue2,y=yValue_cam5,color='camouflage5'))+
#   ggtitle("Original data VS Camouflaged data")+
#   scale_x_continuous("Time", labels = as.character(xValue2), breaks = xValue2)
# 
# ggplot()+geom_line(data = data_original,aes(x=xValue1,y=yValue1,color='orginal'))+
#   geom_line(data = data_camouflage1,aes(x=xValue1,y=yValue_cam1,color='camouflage1'))+
#   geom_line(data = data_camouflage2,aes(x=xValue1,y=yValue_cam2,color='camouflage2'))+
#   geom_line(data = data_camouflage3,aes(x=xValue1,y=yValue_cam3,color='camouflage3'))+
#   geom_line(data = data_camouflage4,aes(x=xValue1,y=yValue_cam4,color='camouflage4'))+
#   geom_line(data = data_camouflage5,aes(x=xValue2,y=yValue_cam5,color='camouflage5'))+
#   ggtitle("Original data VS Camouflaged data")+
#   scale_x_continuous("Time", labels = as.character(xValue2), breaks = xValue2)


