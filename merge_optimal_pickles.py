import pickle
import os

if __name__ == '__main__':
    opt_dict_list = []
    for file_name in os.listdir(os.path.join("optimal_pickles")):
        with open("optimum_output.pickle", "rb") as f:
            opt_dict_list.append(pickle.load(f))

    if opt_dict_list:
        best_output = opt_dict_list[0]
        for opt_dict in opt_dict_list[1:]:
            for key, output_pair in opt_dict:
                if output_pair[1] > best_output[key][1]:
                    best_output[key]= output_pair

        with open('optimum_output.pickle', 'wb') as f:
            pickle.dump(best_output, f)
    