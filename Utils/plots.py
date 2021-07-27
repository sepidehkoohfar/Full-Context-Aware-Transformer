import pickle
import matplotlib.pyplot as plt
import os
import numpy as np
import random
import argparse
import torch.nn as nn


def plot(args, y_true, y_true_input, lstm, attn, attn_conv, attn_temp_cutoff):
    print("plotting...")
    rand_ind = random.randint(0, 8000)
    print(lstm.iloc[rand_ind, :-1])
    print(attn.iloc[rand_ind, :-1])
    plt.rc('axes', labelsize=18)
    plt.rc('axes', titlesize=18)
    plt.rc('legend', fontsize=12)
    plt.plot(np.arange(0, 192), np.concatenate((y_true_input.iloc[rand_ind, :-1], y_true.iloc[rand_ind, :-1])),
             color='blue')
    plt.vlines(168, ymin=0, ymax=max(y_true.iloc[rand_ind, :-1]), colors='lightblue', linestyles="dashed")
    plt.plot(np.arange(168, 192), lstm.iloc[rand_ind, :-1], color='red', linestyle='dashed')
    plt.plot(np.arange(168, 192), attn.iloc[rand_ind, :-1], color='violet', linestyle='dashed')
    plt.plot(np.arange(168, 192), attn_conv.iloc[rand_ind, :-1], color='seagreen', linestyle='dashed')
    plt.plot(np.arange(168, 192), attn_temp_cutoff.iloc[rand_ind, :-1], color='orange', linestyle='dashed')

    plt.title(args.exp_name)
    plt.xlabel('TimeSteps')
    plt.ylabel('Y')
    plt.legend(['ground-truth', 'seq2seq-lstm', 'attn', 'conv attn', 'ours'], loc="upper left")
    plt.savefig('pred_plot_{}.png'.format(args.exp_name))
    plt.close()

def main():

    parser = argparse.ArgumentParser("plots for predictions")
    parser.add_argument("--exp_name", type=str, default="favorita")
    parser.add_argument("--cuda", type=str, default='cuda:0')
    parser.add_argument("--seed", type=int, default=21)
    args = parser.parse_args()

    predictions_lstm = np.zeros((3, 8000, 24))
    predictions_attn = np.zeros((3, 8000, 24))
    predictions_attn_conv = np.zeros((3, 8000, 24))
    predictions_attn_temp = np.zeros((3, 8000, 24))

    y_true = pickle.load(open('y_true_{}.pkl'.format(args.exp_name), 'rb')).values
    print("read y_true")
    '''y_true_input = pickle.load(open('y_true_input_{}.pkl'.format(args.exp_name), 'rb'))
    print("read y_true_input")'''

    seeds = [21, 9, 1992]
    for i, seed in enumerate(seeds):
        predictions_lstm[i, :, :] = pickle.load(open(os.path.join('preds_{}_24'.format(args.exp_name),
                                             'lstm_{}'.format(seed)), 'rb')).values[:, :-1]
        predictions_attn[i, :, :] = pickle.load(open(os.path.join('preds_{}_24'.format(args.exp_name),
                                             'attn_{}'.format(seed)), 'rb')).values[:, :-1]
        predictions_attn_conv[i, :, :] = pickle.load(open(os.path.join('preds_{}_24'.format(args.exp_name),
                                                  'attn_conv_{}'.format(seed)), 'rb')).values[:, :-1]
        predictions_attn_temp[i, :, :] = pickle.load(open(os.path.join('preds_{}_24'.format(args.exp_name), 'attn_temp_cutoff_{}'
                                                         .format(seed)), 'rb')).values[:, :-1]

    RMSE = nn.MSELoss()
    rmse_lstm = np.zeros((3, 24))
    rmse_attn = np.zeros((3, 24))
    rmse_attn_conv = np.zeros((3, 24))
    rmse_attn_temp_cutoff = np.zeros((3, 24))

    for i in range(3):
        for j in range(24):
            rmse_lstm[i, j] = RMSE(y_true[:, j], predictions_lstm[i, :, j])
            rmse_attn[i, j] = RMSE(y_true[:, j], predictions_attn[i, :, j])
            rmse_attn_conv[i, j] = RMSE(y_true[:, j], predictions_attn_conv[i, :, j])
            rmse_attn_temp_cutoff[i, j] = RMSE(y_true[:, j], predictions_attn_temp[i, :, j])

    rmse_lstm = np.mean(rmse_lstm, axis=0)
    rmse_attn = np.mean(rmse_attn, axis=0)
    rmse_attn_conv = np.mean(rmse_attn_conv, axis=0)
    rmse_attn_temp_cutoff = np.mean(rmse_attn_temp_cutoff, axis=0)

    x = np.array([0, 4, 8, 12, 16, 20, 24])
    plt.rc('axes', labelsize=18)
    plt.rc('axes', titlesize=18)
    plt.rc('legend', fontsize=12)
    plt.plot(x, rmse_attn_temp_cutoff[0::4].detach().numpy(), 'xb-', color='deepskyblue')
    plt.plot(x, rmse_attn_conv[0::4].detach().numpy(), 'xb-', color='seagreen')
    plt.plot(x, rmse_attn[0::4].detach().numpy(), 'xb-', color='orange')
    plt.plot(x, rmse_lstm[0::4].detach().numpy(), 'xb-', color='salmon')
    plt.xlabel("Future Timesteps")
    plt.ylabel("RMSE")
    plt.legend(['ours', 'conv attn', 'attn', 'seq2seq-lstm'], loc="upper right")
    name = args.exp_name if args.exp_name != "favorita" else "Retail"
    plt.title(name)
    plt.savefig('rmses_{}.png'.format(name))
    plt.close()


if __name__ == '__main__':
    main()