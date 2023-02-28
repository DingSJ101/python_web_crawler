import bar_chart_race as bcr

# 获取数据
df = bcr.load_dataset('covid19_tutorial')
# print(df)

# 生成GIF图像
bcr.bar_chart_race(df=df,filename='D:/spec_work/能力/可视化/Conv19.mp4')