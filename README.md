# Homework 1 (Color-Transfer and Texture-Transfer)

We organize this report as follow:
1. Training CycleGan
    - describe some modification we made (`deconv` vs. `upsample + conv`)
    - shoing the training loss plot
2. Inferencing
    - visualize/analysis the difference before/after the modification
    - Show some result on personal images
3. Comparison with LAB color transfer


## 1. Training CycleGan
We train CycleGan on `summer2winter_yosemite` dataset. The training detailed and modification we made are summarized as follow:
- We use batch size 8 and input resolution `128x128` to fit our time space constraint.
- All the other hyperparamters are same as original placeholder.
- We tried original `Deconv` and `Upsample + Conv`. Detailed discussion and comparison later.
- We use tensorboardX to monitor the training (see below figures)
    - | Discriminator A | Discriminator B | Generator |
      | :--: | :--: | :--: |
      | ![](assets/DA_loss.png) | ![](assets/DB_loss.png) | ![](assets/G_loss.png) |


## 2. Inferencing
One of the visual defect of original cycle gan is chekerboard artifacts [[ref]](https://distill.pub/2016/deconv-checkerboard/). The reference propose to use `upsample` followed by a `conv` to alleviate the artifact. We tried both `deconv` and `upsample + conv` and showing some of the result as follow:

| Input (winter) | `deconv` CycleGan | `upsample + conv` CycleGan |
| :---: | :------: | :---------------: |
| ![](assets/yomesite/B/input/0178.png) | ![](assets/yomesite/B/deconv/0178.png) | ![](assets/yomesite/B/upconv/0178.png) |
| ![](assets/yomesite/B/input/0195.png) | ![](assets/yomesite/B/deconv/0195.png) | ![](assets/yomesite/B/upconv/0195.png) |
| ![](assets/yomesite/B/input/0232.png) | ![](assets/yomesite/B/deconv/0232.png) | ![](assets/yomesite/B/upconv/0232.png) |
| ![](assets/yomesite/B/input/0250.png) | ![](assets/yomesite/B/deconv/0250.png) | ![](assets/yomesite/B/upconv/0250.png) |
| ![](assets/yomesite/B/input/0308.png) | ![](assets/yomesite/B/deconv/0308.png) | ![](assets/yomesite/B/upconv/0308.png) |

| Input (summer) | `deconv` CycleGan | `upsample + conv` CycleGan |
| :---: | :------: | :---------------: |
| ![](assets/yomesite/A/input/0019.png) | ![](assets/yomesite/A/deconv/0019.png) | ![](assets/yomesite/A/upconv/0019.png) |
| ![](assets/yomesite/A/input/0033.png) | ![](assets/yomesite/A/deconv/0033.png) | ![](assets/yomesite/A/upconv/0033.png) |
| ![](assets/yomesite/A/input/0043.png) | ![](assets/yomesite/A/deconv/0043.png) | ![](assets/yomesite/A/upconv/0043.png) |
| ![](assets/yomesite/A/input/0117.png) | ![](assets/yomesite/A/deconv/0117.png) | ![](assets/yomesite/A/upconv/0117.png) |
| ![](assets/yomesite/A/input/0044.png) | ![](assets/yomesite/A/deconv/0044.png) | ![](assets/yomesite/A/upconv/0044.png) |

From above figures, we observe the `deconv` indeed results more checkerboard artifact than `upsample + conv` does. To further prove the idea, we performe a frequency domain analysis by inspecting the spectrum of 2d discrete fourier transform. We take the mean of all spectrum from normal images, images generated from `deconv` CycleGan and `upsample + conv` CycleGan respectively. Below figures show the mean spectrum of each:

| Normal images | `deconv` CycleGan | `upsample + conv` CycleGan |
| :-----------: | :---------------: | :------------------------: |
| ![](assets/normal_spec.png) | ![](assets/deconv_spec.png) | ![](assets/upconv_spec.png) |

The mean spectrum of normal images is smooth with one spotlight in the middle as expected. The spectrum of `deconv` have a grid arange spotlights in high frequency area which could cause by the so called checkerboard artifacts. Though there is less checkerboard in `upsample + conv`, the spectrum of it have valley in high frequency.

In sum, although the two trained CycleGans are able to transform the style, the artifact are easy to observe if we look detailly.


Below figure showing some result on our captured images by `upsample + conv` CycleGan.

| Scene | Input | to winter | to summer |
| :---: | :---: | :-------: | :-------: |
| 房間窗外 | ![](assets/input/0001.png) | ![](assets/fake_B/0001.png) | ![](assets/fake_A/0001.png) |
| 沖繩水族館 | ![](assets/input/0002.png) | ![](assets/fake_B/0002.png) | ![](assets/fake_A/0002.png) |
| 金瓜石 | ![](assets/input/0003.png) | ![](assets/fake_B/0003.png) | ![](assets/fake_A/0003.png) |

## Comparison with LAB color transfer [[ref]](https://github.com/jrosebr1/color_transfer)

This is a simple method that shifting the target image LAB according to given image where only mean/std are considered in both side. In our implementation, we randomly sample a source image in the training set to tune given target image color. Below show the results compare with CycleGan:

| Input (winter) | `upsample + conv` CycleGan | LAB Color Transfer |
| :---: | :------: | :---------------: |
| ![](assets/yomesite/B/input/0178.png) | ![](assets/yomesite/B/upconv/0178.png) | ![](assets/super_fast/0178.png) |
| ![](assets/yomesite/B/input/0195.png) | ![](assets/yomesite/B/upconv/0195.png) | ![](assets/super_fast/0195.png) |
| ![](assets/yomesite/B/input/0232.png) | ![](assets/yomesite/B/upconv/0232.png) | ![](assets/super_fast/0232.png) |
| ![](assets/yomesite/B/input/0250.png) | ![](assets/yomesite/B/upconv/0250.png) | ![](assets/super_fast/0250.png) |
| ![](assets/yomesite/B/input/0308.png) | ![](assets/yomesite/B/upconv/0308.png) | ![](assets/super_fast/0308.png) |

| Input (summer) | `upsample + conv` CycleGan | LAB Color Transfer |
| :---: | :------: | :---------------: |
| ![](assets/yomesite/A/input/0019.png) | ![](assets/yomesite/A/upconv/0019.png) | ![](assets/super_fast/0019.png) |
| ![](assets/yomesite/A/input/0033.png) | ![](assets/yomesite/A/upconv/0033.png) | ![](assets/super_fast/0033.png) |
| ![](assets/yomesite/A/input/0043.png) | ![](assets/yomesite/A/upconv/0043.png) | ![](assets/super_fast/0043.png) |
| ![](assets/yomesite/A/input/0117.png) | ![](assets/yomesite/A/upconv/0117.png) | ![](assets/super_fast/0117.png) |
| ![](assets/yomesite/A/input/0044.png) | ![](assets/yomesite/A/upconv/0044.png) | ![](assets/super_fast/0044.png) |

The color transfer method perfome well in some of the cases because giving more blue or green could have the people winter/summer feeling. However, if the soure image is not selected carefully, the transfered image will look strange (like the first row in summer2winter table above). Besides, one of the drawback of such color changing method is that it never make new thing. It can't never changing a hourse to zebra. On the other hand, the generative model, here the CycleGan, can make some snow or grass.
