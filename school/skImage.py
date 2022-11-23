from skimage import io
# from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans  # 提升聚类速度
import numpy as np
import sklearn.metrics as sm
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

image = io.imread('故宫.jpg')
io.imshow(image)

data = image / 255.0
data = data.reshape(-1, 3)

SSE = []
silhouette_score = []
k = []
# 簇的数量
colors = [2, 3, 5, 10, 16, 32, 64, 128]
for n_clusters in colors:
    cls = MiniBatchKMeans(n_clusters, batch_size=2048).fit(data)
    score1 = cls.inertia_
    SSE.append(score1)

# 肘部法则，确定聚类个数
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.scatter(range(1, 9), SSE)
ax1.plot(range(1, 9), SSE)
ax1.set_xlabel("colors", fontdict={'fontsize': 15})
ax1.set_ylabel("SSE", fontdict={'fontsize': 15})
ax1.set_xticks(range(1, 9))
for i in range(8):
    plt.text(i + 1, SSE[i], colors[i])

plt.show()

# 运用10个聚类色表示图片
colors_use = 10
km = MiniBatchKMeans(colors_use, batch_size=2048)
km.fit(data)
new_data = km.cluster_centers_[km.predict(data)]  # 利用np.array 的整数索引(高级索引知识)，用聚类中心点值 代替原来点的值

image_new = new_data.reshape(image.shape)
image_new_convert = np.array(np.round(image_new * 255), dtype='uint8')
io.imsave('colors_use_10.jpg', image_new_convert)

# 黑白色表示
new_data = np.array([[255, 255, 255], [0, 0, 0]])[kmeans.predict(data)]
image_new = new_data.reshape(image.shape)
image_new_convert = np.array(np.round(image_new * 255), dtype='uint8')
io.imsave('黑白色.jpg', image_new_convert)
