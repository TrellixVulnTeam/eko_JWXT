# -*- coding: utf-8 -*-
"""
    Convert raw PDF data of :cite:`Giele:2002hx` to Python
"""

# pylint: disable=line-too-long

if __name__ == "__main__":
    # helper to extract the numbers from the pdf
    raw14 = [
        [
            [
                10e-7,
                1.5287e-4,
                1.0244e-4,
                5.7018e-6,
                1.3190e2,
                3.1437e-5,
                6.4877e1,
                6.4161e1,
                9.9763e2,
            ],
            [
                10e-6,
                6.9176e-4,
                4.4284e-4,
                2.5410e-5,
                6.8499e1,
                9.4279e-5,
                3.3397e1,
                3.2828e1,
                4.9124e2,
            ],
            [
                10e-5,
                3.0981e-3,
                1.8974e-3,
                1.0719e-4,
                3.3471e1,
                2.2790e-4,
                1.6059e1,
                1.5607e1,
                2.2297e2,
            ],
            [
                10e-4,
                1.3722e-2,
                8.1019e-3,
                4.2558e-4,
                1.5204e1,
                3.6644e-4,
                7.0670e0,
                6.7097e0,
                9.0668e1,
            ],
            [
                10e-3,
                5.9160e-2,
                3.4050e-2,
                1.6008e-3,
                6.3230e0,
                1.4479e-4,
                2.7474e0,
                2.4704e0,
                3.1349e1,
            ],
            [
                10e-2,
                2.3078e-1,
                1.2919e-1,
                5.5688e-3,
                2.2752e0,
                -5.7311e-4,
                8.5502e-1,
                6.6623e-1,
                8.1381e0,
            ],
            [
                0.1,
                5.5177e-1,
                2.7165e-1,
                1.0023e-2,
                3.9019e-1,
                -3.0627e-4,
                1.1386e-1,
                5.9773e-2,
                9.0563e-1,
            ],
            [
                0.3,
                3.5071e-1,
                1.3025e-1,
                3.0098e-3,
                3.5358e-2,
                -3.1891e-5,
                9.0480e-3,
                3.3061e-3,
                8.4186e-2,
            ],
            [
                0.5,
                1.2117e-1,
                3.1528e-2,
                3.7742e-4,
                2.3867e-3,
                -2.7215e-6,
                5.7965e-4,
                1.7170e-4,
                8.1126e-3,
            ],
            [
                0.7,
                2.0077e-2,
                3.0886e-3,
                1.3434e-5,
                5.4244e-5,
                -1.0106e-7,
                1.2936e-5,
                3.5304e-6,
                3.8948e-4,
            ],
            [
                0.9,
                3.5111e-4,
                1.7783e-5,
                8.651e-9,
                2.695e-8,
                -1.476e-10,
                7.132e-9,
                2.990e-9,
                1.2136e-6,
            ],
        ],
        [
            [
                10e-7,
                1.3416e-4,
                8.7497e-5,
                4.9751e-6,
                1.3020e2,
                2.1524e-5,
                6.4025e1,
                6.3308e1,
                1.0210e3,
            ],
            [
                10e-6,
                6.2804e-4,
                3.9406e-4,
                2.2443e-5,
                6.6914e1,
                6.5149e-5,
                3.2602e1,
                3.2032e1,
                4.9626e2,
            ],
            [
                10e-5,
                2.9032e-3,
                1.7575e-3,
                9.6205e-5,
                3.2497e1,
                1.5858e-4,
                1.5570e1,
                1.5118e1,
                2.2307e2,
            ],
            [
                10e-4,
                1.3206e-2,
                7.7673e-3,
                3.9093e-4,
                1.4751e1,
                2.5665e-4,
                6.8388e0,
                6.4807e0,
                9.0162e1,
            ],
            [
                10e-3,
                5.8047e-2,
                3.3434e-2,
                1.5180e-3,
                6.1703e0,
                1.0388e-4,
                2.6695e0,
                2.3917e0,
                3.1114e1,
            ],
            [
                10e-2,
                2.2930e-1,
                1.2857e-1,
                5.4626e-3,
                2.2492e0,
                -3.9979e-4,
                8.4058e-1,
                6.5087e-1,
                8.0993e0,
            ],
            [
                0.1,
                5.5428e-1,
                2.7326e-1,
                1.0072e-2,
                3.9297e-1,
                -2.1594e-4,
                1.1439e-1,
                5.9713e-2,
                9.0851e-1,
            ],
            [
                0.3,
                3.5501e-1,
                1.3205e-1,
                3.0557e-3,
                3.6008e-2,
                -2.2632e-5,
                9.2227e-3,
                3.3771e-3,
                8.5022e-2,
            ],
            [
                0.5,
                1.2340e-1,
                3.2166e-2,
                3.8590e-4,
                2.4459e-3,
                -1.9420e-6,
                5.9487e-4,
                1.7699e-4,
                8.2293e-3,
            ],
            [
                0.7,
                2.0597e-2,
                3.1751e-3,
                1.3849e-5,
                5.5722e-5,
                -7.2616e-8,
                1.3244e-5,
                3.5361e-6,
                3.9687e-4,
            ],
            [
                0.9,
                3.6527e-4,
                1.8544e-5,
                9.050e-9,
                2.663e-8,
                -1.075e-10,
                6.713e-9,
                2.377e-9,
                1.2489e-6,
            ],
        ],
        [
            [
                10e-7,
                1.7912e-4,
                1.2521e-4,
                6.4933e-6,
                1.2714e2,
                4.9649e-5,
                6.2498e1,
                6.1784e1,
                9.2473e2,
            ],
            [
                10e-6,
                7.7377e-4,
                5.1222e-4,
                2.8719e-5,
                6.7701e1,
                1.4743e-4,
                3.2999e1,
                3.2432e1,
                4.6863e2,
            ],
            [
                10e-5,
                3.3184e-3,
                2.0760e-3,
                1.1977e-4,
                3.3644e1,
                3.5445e-4,
                1.6147e1,
                1.5696e1,
                2.1747e2,
            ],
            [
                10e-4,
                1.4184e-2,
                8.4455e-3,
                4.6630e-4,
                1.5408e1,
                5.6829e-4,
                7.1705e0,
                6.8139e0,
                8.9820e1,
            ],
            [
                10e-3,
                5.9793e-2,
                3.4418e-2,
                1.6996e-3,
                6.4042e0,
                2.2278e-4,
                2.7892e0,
                2.5128e0,
                3.1336e1,
            ],
            [
                10e-2,
                2.3106e-1,
                1.2914e-1,
                5.7016e-3,
                2.2876e0,
                -8.9125e-4,
                8.6205e-1,
                6.7377e-1,
                8.1589e0,
            ],
            [
                0.1,
                5.5039e-1,
                2.7075e-1,
                1.0031e-2,
                3.8850e-1,
                -4.7466e-4,
                1.1332e-1,
                5.9489e-2,
                9.0795e-1,
            ],
            [
                0.3,
                3.4890e-1,
                1.2949e-1,
                2.9943e-3,
                3.5090e-2,
                -4.9304e-5,
                8.9667e-3,
                3.2670e-3,
                8.4309e-2,
            ],
            [
                0.5,
                1.2026e-1,
                3.1269e-2,
                3.7428e-4,
                2.3729e-3,
                -4.1981e-6,
                5.7783e-4,
                1.7390e-4,
                8.1099e-3,
            ],
            [
                0.7,
                1.9867e-2,
                3.0534e-3,
                1.3273e-5,
                5.4635e-5,
                -1.5541e-7,
                1.3275e-5,
                3.9930e-6,
                3.8824e-4,
            ],
            [
                0.9,
                3.4524e-4,
                1.7466e-5,
                8.489e-9,
                3.030e-8,
                -2.255e-10,
                8.863e-9,
                4.803e-9,
                1.2026e-6,
            ],
        ],
    ]

    raw15 = [
        [
            [
                10e-7,
                1.5978e-4,
                1.0699e-5,
                6.0090e-6,
                1.3916e2,
                6.8509e1,
                6.6929e1,
                5.7438e1,
                9.9694e3,
            ],
            [
                10e-6,
                7.1787e-4,
                4.5929e-4,
                2.6569e-5,
                7.1710e1,
                3.5003e1,
                3.3849e1,
                2.8332e1,
                4.8817e2,
            ],
            [
                10e-5,
                3.1907e-3,
                1.9532e-3,
                1.1116e-4,
                3.4732e1,
                1.6690e1,
                1.5875e1,
                1.2896e1,
                2.2012e2,
            ],
            [
                10e-4,
                1.4023e-2,
                8.2749e-3,
                4.3744e-4,
                1.5617e1,
                7.2747e0,
                6.7244e0,
                5.2597e0,
                8.8804e1,
            ],
            [
                10e-3,
                6.0019e-2,
                3.4519e-2,
                1.6296e-3,
                6.4173e0,
                2.7954e0,
                2.4494e0,
                1.8139e0,
                3.0404e1,
            ],
            [
                10e-2,
                2.3244e-1,
                1.3000e-1,
                5.6100e-3,
                2.2778e0,
                8.5749e-1,
                6.6746e-1,
                4.5073e-1,
                7.7912e0,
            ],
            [
                0.1,
                5.4993e-1,
                2.7035e-1,
                9.9596e-3,
                3.8526e-1,
                1.1230e-1,
                6.4466e-2,
                3.7280e-2,
                8.5266e-1,
            ],
            [
                0.3,
                3.4622e-1,
                1.2833e-1,
                2.9572e-3,
                3.4600e-2,
                8.8410e-3,
                4.0134e-3,
                2.1047e-3,
                7.8898e-2,
            ],
            [
                0.5,
                1.1868e-1,
                3.0811e-2,
                3.6760e-4,
                2.3198e-3,
                5.6309e-4,
                2.3752e-4,
                1.2004e-4,
                7.6398e-3,
            ],
            [
                0.7,
                1.9486e-2,
                2.9901e-3,
                1.2957e-5,
                5.2352e-5,
                1.2504e-5,
                5.6038e-6,
                2.8888e-6,
                3.7080e-4,
            ],
            [
                0.9,
                3.3522e-4,
                1.6933e-5,
                8.209e-9,
                2.574e-8,
                6.856e-9,
                4.337e-9,
                2.679e-9,
                1.1721e-6,
            ],
        ],
        [
            [
                10e-7,
                1.3950e-4,
                9.0954e-5,
                5.2113e-6,
                1.3549e2,
                6.6672e1,
                6.5348e1,
                5.6851e1,
                1.0084e3,
            ],
            [
                10e-6,
                6.4865e-4,
                4.0691e-4,
                2.3344e-5,
                6.9214e1,
                3.3753e1,
                3.2772e1,
                2.7818e1,
                4.8816e2,
            ],
            [
                10e-5,
                2.9777e-3,
                1.8020e-3,
                9.9329e-5,
                3.3385e1,
                1.6015e1,
                1.5306e1,
                1.2601e1,
                2.1838e2,
            ],
            [
                10e-4,
                1.3452e-2,
                7.9078e-3,
                4.0036e-4,
                1.5035e1,
                6.9818e0,
                6.4880e0,
                5.1327e0,
                8.7550e1,
            ],
            [
                10e-3,
                5.8746e-2,
                3.3815e-2,
                1.5411e-3,
                6.2321e0,
                2.7012e0,
                2.3747e0,
                1.7742e0,
                3.0060e1,
            ],
            [
                10e-2,
                2.3063e-1,
                1.2923e-1,
                5.4954e-3,
                2.2490e0,
                8.4141e-1,
                6.5083e-1,
                4.4354e-1,
                7.7495e0,
            ],
            [
                0.1,
                5.5279e-1,
                2.7222e-1,
                1.0021e-2,
                3.8897e-1,
                1.1312e-1,
                6.2917e-2,
                3.7048e-2,
                8.5897e-1,
            ],
            [
                0.3,
                3.5141e-1,
                1.3051e-1,
                3.0134e-3,
                3.5398e-2,
                9.0559e-3,
                3.8727e-3,
                2.0993e-3,
                8.0226e-2,
            ],
            [
                0.5,
                1.2140e-1,
                3.1590e-2,
                3.7799e-4,
                2.3919e-3,
                5.8148e-4,
                2.2376e-4,
                1.1918e-4,
                7.8098e-3,
            ],
            [
                0.7,
                2.0120e-2,
                3.0955e-3,
                1.3462e-5,
                5.4194e-5,
                1.2896e-5,
                5.0329e-6,
                2.8153e-6,
                3.8099e-4,
            ],
            [
                0.9,
                3.5230e-4,
                1.7849e-5,
                8.687e-9,
                2.568e-8,
                6.513e-9,
                3.390e-9,
                2.407e-9,
                1.2188e-6,
            ],
        ],
        [
            [
                10e-7,
                1.8906e-4,
                1.3200e-4,
                6.9268e-6,
                1.3739e2,
                6.7627e1,
                6.5548e1,
                5.5295e1,
                9.4403e2,
            ],
            [
                10e-6,
                8.1001e-4,
                5.3574e-4,
                3.0345e-5,
                7.2374e1,
                3.5337e1,
                3.3846e1,
                2.7870e1,
                4.7444e2,
            ],
            [
                10e-5,
                3.4428e-3,
                2.1524e-3,
                1.2531e-4,
                3.5529e1,
                1.7091e1,
                1.6065e1,
                1.2883e1,
                2.1802e2,
            ],
            [
                10e-4,
                1.4580e-2,
                8.6744e-3,
                4.8276e-4,
                1.6042e1,
                7.4886e0,
                6.8276e0,
                5.3044e0,
                8.9013e1,
            ],
            [
                10e-3,
                6.0912e-2,
                3.5030e-2,
                1.7393e-3,
                6.5544e0,
                2.8656e0,
                2.4802e0,
                1.8362e0,
                3.0617e1,
            ],
            [
                10e-2,
                2.3327e-1,
                1.3022e-1,
                5.7588e-3,
                2.2949e0,
                8.6723e-1,
                6.7688e-1,
                4.5597e-1,
                7.8243e0,
            ],
            [
                0.1,
                5.4798e-1,
                2.6905e-1,
                9.9470e-3,
                3.8192e-1,
                1.1124e-1,
                6.7091e-2,
                3.7698e-2,
                8.4908e-1,
            ],
            [
                0.3,
                3.4291e-1,
                1.2693e-1,
                2.9239e-3,
                3.4069e-2,
                8.6867e-3,
                4.3924e-3,
                2.1435e-3,
                7.8109e-2,
            ],
            [
                0.5,
                1.1694e-1,
                3.0310e-2,
                3.6112e-4,
                2.2828e-3,
                5.5537e-4,
                2.7744e-4,
                1.2416e-4,
                7.5371e-3,
            ],
            [
                0.7,
                1.9076e-2,
                2.9217e-3,
                1.2635e-5,
                5.2061e-5,
                1.2677e-5,
                7.2083e-6,
                3.0908e-6,
                3.6441e-4,
            ],
            [
                0.9,
                3.2404e-4,
                1.6333e-5,
                7.900e-9,
                2.850e-8,
                8.407e-9,
                6.795e-9,
                3.205e-9,
                1.1411e-6,
            ],
        ],
    ]

    outs = {}
    cnt = 0
    for r in raw15:
        cnt += 1
        outs[f"part{cnt}"] = []
        out = {
            "x": [],
            "u_v": [],
            "d_v": [],
            "L_m": [],
            "L_p": [],
            "s_v": [],
            "s_p": [],
            "c_p": [],
            "g": [],
        }
        for line in r:
            out["x"].append(line[0])
            out["u_v"].append(line[1])
            out["d_v"].append(line[2])
            out["L_m"].append(line[3])
            out["L_p"].append(line[4])
            out["s_v"].append(line[5])
            out["s_p"].append(line[6])
            out["c_p"].append(line[7])
            out["g"].append(line[8])
        outs[f"part{cnt}"].append(out)
    print(outs)
