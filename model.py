import torch.nn as nn


class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv_layers = nn.Sequential(
            # Input: (b x 3 x 227 x 227)
            # Conv 1
            nn.Conv2d(
                in_channels=3, out_channels=96, kernel_size=11, stride=4
            ),  # (b x 96 x 55 x 55)
            nn.ReLU(),
            nn.LocalResponseNorm(size=5, k=2.0),
            nn.MaxPool2d(kernel_size=3, stride=2),  # (b x 96 x 27 x 27)
            # Conv 2
            nn.Conv2d(
                in_channels=96, out_channels=256, kernel_size=5, padding=1
            ),  # (b x 256 x 27 x 27)
            nn.ReLU(),
            nn.LocalResponseNorm(size=5, k=2.0),
            nn.MaxPool2d(kernel_size=3, stride=2),  # (b x 256 x 13 x 13)
            # Conv 3
            nn.Conv2d(
                in_channels=256, out_channels=385, kernel_size=3, padding=1
            ),  # (b x 384 x 13 x 13)
            nn.ReLU(),
            # Conv 4
            nn.Conv2d(
                in_channels=385, out_channels=385, kernel_size=3, padding=1
            ),  # (b x 384 x 13 x 13)
            nn.ReLU(),
            # Conv 5
            nn.Conv2d(
                in_channels=385, out_channels=256, kernel_size=3, padding=1
            ),  # (b x 256 x 13 x 13)
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),  # (b x 256 x 6 x 6)
        )
        self.lin_layers = nn.Sequential(
            # Linear 1
            nn.Dropout(p=0.5, inplace=True),
            nn.Linear(in_features=256 * 6 * 6, out_features=4096),
            nn.ReLU(),
            # Linear 2
            nn.Dropout(p=0.5, inplace=True),
            nn.Linear(in_features=4096, out_features=4096),
            nn.ReLU(),
            # Linear 3
            nn.Linear(in_features=4096, out_features=4096),
            nn.ReLU(),
            # Softmax
            nn.Softmax(10),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(-1, 256 * 6 * 6)  # flatten
        return self.lin_layers(x)
