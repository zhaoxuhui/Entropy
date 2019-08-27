#include <iostream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

struct IJpair {
    // 自定义IJpair数据格式用于存放数值对
    // 同时重载了==和<使其可以进行大小比较

    int center_p;
    int mean_p;

    bool operator==(const IJpair &ij) const {
        return center_p == ij.center_p && mean_p == ij.mean_p;
    }

    // 比较大小的规则是center_p小的在前，center_p相同时mean_p小的在前
    bool operator<(const IJpair &ij) const {
        if (center_p < ij.center_p) {
            return true;
        } else if (center_p == ij.center_p) {
            if (mean_p < ij.mean_p) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
};

// 为影像块计算IJ元组
IJpair calcIJ(Mat img_patch) {
    int total_p = img_patch.rows * img_patch.cols;
    if (total_p % 2 != 0) {
        int center_p = img_patch.at<uchar>(img_patch.rows / 2, img_patch.cols / 2);
        int mean_p = (sum(img_patch).val[0] - center_p) / (total_p - 1);
        return IJpair{center_p, mean_p};
    } else {
        cout << "error" << endl;
    }
}

// 按照算法计算每个元组出现的次数
vector<int> calcFij(vector<IJpair> &tup_list) {
    sort(tup_list.begin(), tup_list.end());
    vector<int> times;
    times.push_back(0);
    for (int i = 0; i < tup_list.size() - 1; ++i) {
        if (tup_list[i] == tup_list[i + 1]) {
            times.push_back(1);
        } else {
            times.push_back(0);
        }
    }

    vector<int> times2;
    int sum = 0;
    for (int j = 0; j < times.size() - 1; ++j) {
        if (times[j] == 0 and times[j + 1] == 0) {
            times2.push_back(times[j] + 1);
        } else if (times[j] == 1 and times[j + 1] == 0) {
            times2.push_back(sum + 1);
            sum = 0;
        } else {
            sum += 1;
            if (j == times.size() - 2) {
                times2.push_back(sum + 1);
            }
        }
    }
    if (times[-1] == 0) {
        times2.push_back(1);
    }
    return times2;
}

// 计算一张影像的二维熵
double calcEntropy2d(Mat img, int win_w = 3, int win_h = 3) {
    int ext_x = win_w / 2;
    int ext_y = win_h / 2;

    Mat final_img;
    copyMakeBorder(img, final_img, ext_y, ext_y, ext_x, ext_x, BORDER_CONSTANT, Scalar(0));

    int new_width = final_img.cols;
    int new_height = final_img.rows;

    clock_t t1 = clock();
    vector<IJpair> IJs;
    for (int i = ext_x; i < new_width - ext_x; ++i) {
        for (int j = ext_y; j < new_height - ext_y; ++j) {
            Mat patch(final_img, Rect(i - ext_x, j - ext_y, 2 * ext_x + 1, 2 * ext_y + 1));
            IJpair tmp = calcIJ(patch);
            IJs.push_back(tmp);
        }
    }
    clock_t t2 = clock();
    double dt1 = (t2 - t1) * 1.0 / CLOCKS_PER_SEC;
    printf("calc IJ time %.10lf\n", dt1);

    vector<int> Fij;
    cout << "start calculating..." << endl;
    clock_t t3 = clock();
    Fij = calcFij(IJs);
    clock_t t4 = clock();
    double dt2 = (t4 - t3) * 1.0 / CLOCKS_PER_SEC;
    printf("IJpair len %ld,Fij len %ld\n", IJs.size(), Fij.size());
    printf("fij time %.10lf\n", dt2);

    clock_t t5 = clock();
    vector<double> Pij;
    double tmp_p;
    for (int k = 0; k < Fij.size(); ++k) {
        tmp_p = Fij[k] * 1.0 / (new_height * new_width * 1.0);
        Pij.push_back(tmp_p);
    }
    clock_t t6 = clock();
    double dt3 = (t6 - t5) * 1.0 / CLOCKS_PER_SEC;
    printf("pij time %.10lf\n", dt3);

    clock_t t7 = clock();
    vector<double> H_tem;
    double H;
    for (int l = 0; l < Pij.size(); ++l) {
        double h_tem = -Pij[l] * (log(Pij[l]) / log(2));
        H_tem.push_back(h_tem);
        H += h_tem;
    }
    clock_t t8 = clock();
    double dt4 = (t8 - t7) * 1.0 / CLOCKS_PER_SEC;
    printf("h tem time %.10lf\n", dt4);
    return H;
}


int main() {
    Mat img = imread("../../imgs/img4.jpg", IMREAD_GRAYSCALE);
    clock_t t1 = clock();
    double H = calcEntropy2d(img, 3, 3);
    clock_t t2 = clock();
    double dt = (t2 - t1) * 1.0 / CLOCKS_PER_SEC;
    printf("\nall time %.10lf\n", dt);
    printf("H %.15lf\n", H);
    return 0;
}