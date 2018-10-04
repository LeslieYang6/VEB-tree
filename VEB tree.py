import math


class VEB:
    def __init__(self, u):
        if not u > 0:
            raise KeyError()
        self.u = 2
        while self.u < u:
            self.u *= self.u
        if self.u > 2:
            self.clusters=[]
            for i in range(int(math.sqrt(self.u))):
                self.clusters.append(VEB(self.high(self.u)))
            self.summary = VEB(self.high(u))
        self.max = self.min = None

    def high(self, x):
        return int(math.floor(x / math.sqrt(self.u)))

    def low(self, x):
        return int(x % math.sqrt(self.u))

    def index(self, i, j):
        return int(i * math.sqrt(self.u) + j)

    def insert(self, x):
        # 解决base case
        if self.u == 2:
            # 如果出现了重复插入，直接返回
            if self.max is not None and self.min != self.max:
                return
            if self.min is None:
                self.max = self.min = x
            else:
                if x > self.min:
                    self.max = x
                else:
                    self.min, self.max = x, self.min
            return
        # 利用空cluster的插入时将插入值放入self.min中，完成lglgu时间的算法
        if self.min is None:
            self.max = self.min = x
            return
        # 交换x,和self.min
        if x < self.min:
            self.min, x = x, self.min
        # 设置self.max
        if x > self.max:
            self.max = x
        # 进入此循环后，下一个cluster的循环会在第一次递归的时候退出
        if self.clusters[self.high(x)].min is None:
            self.summary.insert(self.high(x))
        self.clusters[self.high(x)].insert(self.low(x))

    # delete的对象不同有不同的处理办法
    def delete(self, x):
        # 处理base case
        if self.u==2:
            if self.min==self.max:
                self.min=self.max=None
            else:
                if self.min==x:
                    self.min=self.max
                else:
                    self.max=self.min
            return
        # 被删除为self.min,需要寻找它的successor
        if x == self.min:
            i = self.summary.min
            if i is None:
                self.min = self.max = None
                return
            else:
                x = self.min = self.index(i, self.clusters[i].min)
        self.clusters[self.high(x)].delete(self.low(x))
        if self.clusters[self.high(x)].min is None:
            self.summary.delete(self.high(x))
        if x == self.max:
            i = self.summary.max
            if i is None:
                self.max=self.min
            else:
                i = self.summary.max
                self.max = self.index(i, self.clusters[i].max)


    # 寻找successor
    def successor(self, x):
        if self.u==2:
            return self.max
        # 处理x小于最小值的情况
        if x<self.min:
            return self.min
        if self.clusters[self.high(x)].max is not None and self.clusters[self.high(x)].max>self.low(x):
            return self.index(self.high(x),self.clusters[self.high(x)].successor(self.low(x)))
        else:
            p=self.summary.successor(self.high(x))
            return self.index(p,self.clusters[p].min)


p=VEB(2000)
for i in range(2000):
    p.insert(i)
p.delete(1556)
print(p.successor(1555))
