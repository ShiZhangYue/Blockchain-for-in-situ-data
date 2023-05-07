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
data_camouflage=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/camouflage data.csv',header = FALSE)
data_original=read.csv(file='D:/Onedrive/OneDrive - Oklahoma A and M System/Zhangyue/Code Library/Blockchain for in-situ data/Blockchain-for-in-situ-data/original data.csv',header = FALSE)


xValue1 <- 1:10
xValue2 <- 1:12
yValue1 <- data_original[[1]]
yValue2 <- -data_camouflage[[1]]/1e8

yValue_cam1 <- data_camouflage[[1]][1:10]/1e8
yValue_cam2 <- data_camouflage[[1]][11:20]/1e8
yValue_cam3 <- data_camouflage[[1]][21:30]/1e8
yValue_cam4 <- data_camouflage[[1]][31:40]/1e8
yValue_cam5 <- data_camouflage[[1]][41:52]/1e8


data_original=data.frame(xValue1,yValue1)
data_camouflage1=data.frame(xValue1,yValue_cam1)
data_camouflage2=data.frame(xValue1,yValue_cam2)
data_camouflage3=data.frame(xValue1,yValue_cam3)
data_camouflage4=data.frame(xValue1,yValue_cam4)
data_camouflage5=data.frame(xValue2,yValue_cam5)

ggplot()+geom_line(data = data_original,aes(x=xValue1,y=yValue1,color='yValue1'))+
  geom_point(data = data_original,aes(x=xValue1,y=yValue1))
                  
ggplot()+geom_line(data = data_camouflage,aes(x=xValue2,y=yValue2,color='yValue2'),color='blue')+
  geom_point(data = data_camouflage,aes(x=xValue2,y=yValue2))

ggplot()+geom_line(data = data_original,aes(x=xValue1,y=yValue1,color='orginal'))+
  geom_line(data = data_camouflage1,aes(x=xValue1,y=yValue_cam1,color='camouflage1'))+
  geom_line(data = data_camouflage2,aes(x=xValue1,y=yValue_cam2,color='camouflage2'))+
  geom_line(data = data_camouflage3,aes(x=xValue1,y=yValue_cam3,color='camouflage3'))+
  geom_line(data = data_camouflage4,aes(x=xValue1,y=yValue_cam4,color='camouflage4'))+
  geom_line(data = data_camouflage5,aes(x=xValue2,y=yValue_cam5,color='camouflage5'))+
  ggtitle("Original data VS Camouflaged data")

