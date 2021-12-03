import pickle
import os

if __name__ == '__main__':
    opt_dict_list = []
    for file_name in os.listdir(os.path.join("optimal_pickles")):
        with open(os.path.join("optimal_pickles", file_name), "rb") as f:
            if file_name[0] != ".":
                print(os.path.join("optimal_pickles", file_name))
                opt_dict_list.append(pickle.load(f))

    if opt_dict_list:
        best_output = opt_dict_list[0]
        for opt_dict in opt_dict_list[1:]:
            for key, output_pair in opt_dict.items():
                if output_pair[1] > best_output[key][1]:
                    best_output[key]= output_pair

        with open('optimum_output.pickle', 'wb') as f:
            pickle.dump(best_output, f)
        
        total_benefit = 0.0
        for key, output_pair in best_output.items():
            total_benefit += output_pair[1]
        print(total_benefit)
    