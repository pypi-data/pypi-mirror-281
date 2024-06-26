import torch
import torch.nn as nn

# USRCNN Generator
class USRGAN(nn.Module):
    def __init__(self):
        super(USRGAN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn3 = nn.BatchNorm2d(3)
        self.conv4 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn4 = nn.BatchNorm2d(64)
        self.relu3 = nn.ReLU()
        self.conv5 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn5 = nn.BatchNorm2d(32)
        self.relu4 = nn.ReLU()
        self.conv6 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn6 = nn.BatchNorm2d(3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu1(self.bn1(self.conv1(x)))
        x = self.relu2(self.bn2(self.conv2(x)))
        x = self.sigmoid(self.bn3(self.conv3(x)))
        x = self.relu3(self.bn4(self.conv4(x)))
        x = self.relu4(self.bn5(self.conv5(x)))
        x = self.sigmoid(self.bn6(self.conv6(x)))
        return x

# ESRCNN Generator
class ESRGAN(nn.Module):
    def __init__(self, num_channels=3):
        super(ESRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(num_channels, 64, kernel_size=9, padding=9 // 2),
            nn.ReLU(inplace=True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, kernel_size=5, padding=5 // 2),
            nn.ReLU(inplace=True)
        )
        self.reconstruction = nn.Conv2d(32, num_channels, kernel_size=5, padding=5 // 2)

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# BSRCNN Generator
class BSRGAN(nn.Module):
    def __init__(self):
        super(BSRGAN, self).__init__()
        self.layer1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn3 = nn.BatchNorm2d(3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu1(self.bn1(self.layer1(x)))
        x = self.relu2(self.bn2(self.layer2(x)))
        x = self.sigmoid(self.bn3(self.layer3(x)))
        return x

# ISRCNN Generator
class ISRGAN(nn.Module):
    def __init__(self):
        super(ISRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, (9, 9), (1, 1), (4, 4)),
            nn.BatchNorm2d(64),
            nn.ReLU(True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, (5, 5), (1, 1), (2, 2)),
            nn.BatchNorm2d(32),
            nn.ReLU(True)
        )
        self.reconstruction = nn.Conv2d(32, 3, (5, 5), (1, 1), (2, 2))

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# RSRCNN Generator
class RSRGAN(nn.Module):
    def __init__(self):
        super(RSRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, (9, 9), (1, 1), (4, 4)),
            nn.ReLU(True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, (5, 5), (1, 1), (2, 2)),
            nn.ReLU(True)
        )
        self.reconstruction = nn.Conv2d(32, 3, (5, 5), (1, 1), (2, 2))

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# SRCNN Generator
class SRGAN(nn.Module):
    def __init__(self):
        super(SRGAN, self).__init__()
        self.layer1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)

    def forward(self, x):
        x = self.relu1(self.layer1(x))
        x = self.relu2(self.layer2(x))
        x = torch.sigmoid(self.layer3(x))
        return x

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.fc1 = nn.Linear(512 * 4 * 4, 1)
        self.sigmoid = nn.Sigmoid()

    import torch
import torch.nn as nn

# USRCNN Generator
class USRGAN(nn.Module):
    def __init__(self):
        super(USRGAN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn3 = nn.BatchNorm2d(3)
        self.conv4 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn4 = nn.BatchNorm2d(64)
        self.relu3 = nn.ReLU()
        self.conv5 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn5 = nn.BatchNorm2d(32)
        self.relu4 = nn.ReLU()
        self.conv6 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn6 = nn.BatchNorm2d(3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu1(self.bn1(self.conv1(x)))
        x = self.relu2(self.bn2(self.conv2(x)))
        x = self.sigmoid(self.bn3(self.conv3(x)))
        x = self.relu3(self.bn4(self.conv4(x)))
        x = self.relu4(self.bn5(self.conv5(x)))
        x = self.sigmoid(self.bn6(self.conv6(x)))
        return x

# ESRCNN Generator
class ESRGAN(nn.Module):
    def __init__(self, num_channels=3):
        super(ESRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(num_channels, 64, kernel_size=9, padding=9 // 2),
            nn.ReLU(inplace=True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, kernel_size=5, padding=5 // 2),
            nn.ReLU(inplace=True)
        )
        self.reconstruction = nn.Conv2d(32, num_channels, kernel_size=5, padding=5 // 2)

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# BSRCNN Generator
class BSRGAN(nn.Module):
    def __init__(self):
        super(BSRGAN, self).__init__()
        self.layer1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.bn2 = nn.BatchNorm2d(32)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        self.bn3 = nn.BatchNorm2d(3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu1(self.bn1(self.layer1(x)))
        x = self.relu2(self.bn2(self.layer2(x)))
        x = self.sigmoid(self.bn3(self.layer3(x)))
        return x

# ISRCNN Generator
class ISRGAN(nn.Module):
    def __init__(self):
        super(ISRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, (9, 9), (1, 1), (4, 4)),
            nn.BatchNorm2d(64),
            nn.ReLU(True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, (5, 5), (1, 1), (2, 2)),
            nn.BatchNorm2d(32),
            nn.ReLU(True)
        )
        self.reconstruction = nn.Conv2d(32, 3, (5, 5), (1, 1), (2, 2))

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# RSRCNN Generator
class RSRGAN(nn.Module):
    def __init__(self):
        super(RSRGAN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, (9, 9), (1, 1), (4, 4)),
            nn.ReLU(True)
        )
        self.map = nn.Sequential(
            nn.Conv2d(64, 32, (5, 5), (1, 1), (2, 2)),
            nn.ReLU(True)
        )
        self.reconstruction = nn.Conv2d(32, 3, (5, 5), (1, 1), (2, 2))

    def forward(self, x):
        out = self.features(x)
        out = self.map(out)
        out = self.reconstruction(out)
        return out

# SRCNN Generator
class SRGAN(nn.Module):
    def __init__(self):
        super(SRGAN, self).__init__()
        self.layer1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.relu1 = nn.ReLU()
        self.layer2 = nn.Conv2d(64, 32, kernel_size=5, padding=2)
        self.relu2 = nn.ReLU()
        self.layer3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)

    def forward(self, x):
        x = self.relu1(self.layer1(x))
        x = self.relu2(self.layer2(x))
        x = torch.sigmoid(self.layer3(x))
        return x

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True)
        )
        self.fc1 = nn.Linear(512 * 4 * 4, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.sigmoid(x)
        return x
