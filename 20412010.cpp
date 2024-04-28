
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstring>
#include <ctime>

using namespace std;

int MAX_TIME = 30;  // the maximum running time for each problem instance

// This class is about an item in a bin
class Item{
public:
    // Constructor of Item
    Item(int size, int index){
        item_size = size;
        item_index = index;
    }
    // This function is the getter of item_size
    int get_ItemSize(){
        return item_size;
    }
    // This funciton is the gettrt of item_index
    int get_ItemIndex(){
        return item_index;
    }
private:
    int item_size;
    int item_index;
};

// This class is about a bin to contain items
class Bin{
public:
    int capacity_left;
    vector<Item> items;

    // Constructor of Bin
    Bin(int capacity){
        capacity_left = capacity;
    }
};

// This class is about a problem to be solved
class Problem{
public:
    vector<Item> items;
    string name;
    int item_number;
    int bin_capacity;
    float best_objective;
};

// This class is about a solution for a problem
class Solution{
public: 
    Problem problem;
    float objective;
    int feasibility;
    vector<Bin> bins;

};

// This class is about mainly solving problems using VNS
class My_problems{
public: 
    // This function is used for initializing all the problems
    void initial_problems(int problem_number){
        for(int i=0; i<problem_number; i++){
            Problem problem;
            my_problems.push_back(problem);
        }
    }

    // This funciton is used for loading the problems from the input file
    void load_problems(string data_file){
        
        ifstream openfile;
        openfile.open(data_file);
        if(! openfile.is_open()){
            cout << "Data file "+data_file+" does not exist. Please check!\n" << endl;
            exit(2);
        }

        int temp;
        string str_temp;
        openfile >> temp;
        problem_number = temp;

        //  initial problems
        initial_problems(problem_number);   

        for(int i = 0; i<problem_number; i++){

            openfile >> str_temp;
            my_problems[i].name = str_temp;

            openfile >> temp;
            my_problems[i].bin_capacity = temp;

            openfile >> temp;
            my_problems[i].item_number = temp;
    
            openfile >> temp;
            my_problems[i].best_objective = temp;

            for(int j=0; j<my_problems[i].item_number; j++){
                openfile >> temp;
                Item item(temp, j);
                my_problems[i].items.push_back(item);
            }
        }
        openfile.close();
    }

    // This comparation function is used to compare two item sizes
    // If the size of item1 is smaller than the size of item2, return true, else false.
    static bool itemCmp(Item item1, Item item2){
        if(item1.get_ItemSize()>item2.get_ItemSize())
        {
            return true;
        }
        else{
            return false;
        }
    }
    // This comparation function is used to compare two item sizes
    // If the size of item2 is smaller than the size of item1, return true, else false.

    // This comparation function is used to compare left capacities of two bins
    // If the left capacity of bin1 is smaller than the left capacity of bin2, reutrn true, else return false.
    static bool binCmp(Bin bin1, Bin bin2){
        if(bin1.capacity_left < bin2.capacity_left)
        {
            return true;
        }
        else{
            return false;
        }
    }

    // This fuction is used to check if there is a empty bin in the bins. 
    // If there is an empty bin, remove it.
    void emptybin_checker(Solution &solution){
        for(int i=0; i<solution.bins.size(); i++){
            if(solution.bins[i].items.size()== 0){
                solution.bins.erase(solution.bins.begin()+i);
                i--;
            }
        }
    }

    // Shift heuristic method
    // Select each item from the bin with the largest residual capacity and 
    // try to move the items to the rest of the bins using the best fit descent heuristic.
    void ShiftStrategy(Solution &solution){
        vector<Bin> sorted_bins;
        sorted_bins = solution.bins;
        sort(sorted_bins.begin(), sorted_bins.end(), binCmp);  // sort bins from small left capacity to big left capacity
        //best fit
        for(int i = 0; i < sorted_bins.back().items.size(); i++)
        {
            for(int j = 0; j < sorted_bins.size()-1; j++)  // look for the target bin with the smallest capacity that fits the item
            {
                if(sorted_bins.back().items[i].get_ItemSize() <= sorted_bins[j].capacity_left)
                {
                    sorted_bins[j].items.push_back(sorted_bins.back().items[i]);    // shift the item to the target bin
                    sorted_bins[j].capacity_left -= sorted_bins.back().items[i].get_ItemSize();
                    sort(sorted_bins[j].items.rbegin(), sorted_bins[j].items.rend(), itemCmp);    // sort the bin with shifted item from big size to small size
                    sorted_bins.back().capacity_left += sorted_bins.back().items[i].get_ItemSize();
                    sorted_bins.back().items.erase(sorted_bins.back().items.begin()+i);     // delete the item from the original bin
                    i--;    // because of the deletion of the item, the index back to the previous one
                    if(sorted_bins.back().items.size()==0)
                    {
                        sorted_bins.pop_back();
                    }
                    break;
                }
            }
        }
        solution.bins = sorted_bins;
        solution.objective = solution.bins.size(); 
        emptybin_checker(solution);   //check the empty bin
    }

    // Split heuristic method
    // Move half the items (randomly selected from) the current bin to a new bin
    // if the number of items in the current bin exceeds the average item numbers per bin.
    void SplitStrategy(Solution &solution){
        int avg_mum_item = solution.problem.item_number/solution.bins.size();   // average item numbers per bin
        int num_split;  
        for(int i=0; i<solution.bins.size(); i++){
            if(solution.bins[i].items.size() > avg_mum_item){
                num_split = solution.bins[i].items.size()/2;
                random_shuffle(solution.bins[i].items.begin(), solution.bins[i].items.end());   // shuffle the items which will be repacked
                Bin bin(solution.problem.bin_capacity);
                for(int j=0; j<num_split; j++){
                    bin.items.push_back(solution.bins[i].items[j]);     // move the item from the current bin to a new bin
                    solution.bins[i].capacity_left += solution.bins[i].items[j].get_ItemSize();
                    bin.capacity_left -= solution.bins[i].items[j].get_ItemSize();
                }
                solution.bins[i].items.erase(solution.bins[i].items.begin(), solution.bins[i].items.begin()+num_split); // delete the chosen items from the current bin
                sort(bin.items.rbegin(), bin.items.rend(), itemCmp);    // sort the
                sort(solution.bins[i].items.rbegin(), solution.bins[i].items.rend(), itemCmp);
                solution.bins.push_back(bin);
                break;
            }
        }
        solution.objective = solution.bins.size();
    }

    // Exchange largestBin_largestItem heuristic method
    // Exchange the largest item in the largest left capacity bin with the items which are in a radom bin and can be exchanged into the current bin
    void Exchange_LBLI(Solution &solution){
        emptybin_checker(solution); // check the empty bin
        bool flag = false;       //successfully exchanged flag
        vector<Bin> sorted_bins;
        sorted_bins = solution.bins;
        sort(sorted_bins.rbegin(), sorted_bins.rend(), binCmp);  // sort bins from big left capacity to small left capacity
        // record all the indexes of the bin which is not full
        vector<int> unfull_index;
        for(int i=1; i<sorted_bins.size(); i++)
        {
            if(sorted_bins[i].capacity_left>0){
                unfull_index.push_back(i);
            }
        }
        int target_index = unfull_index[rand() % unfull_index.size()]; // get the index of a random bin which is not full
        vector<Item> target_items;      // a temporary items to store the items will be exchanged
        vector<int> target_indexes;
        // Because the bins and items of each bin have been sorted from big one to small one,
        // the largest item from the bin with the largest residual capacity is the first item of the first bins.
        bool can_exchange1 = false;
        bool can_exchange2 = false;
        sort(sorted_bins[0].items.rbegin(), sorted_bins[0].items.rend(), itemCmp);  // sort the items from large one to small one in the bin with the largest left capacity
        int current_size = sorted_bins[0].items[0].get_ItemSize();
        int sum_size = 0;     //sum of the size of the target items
        for (int i = 0; i < sorted_bins[target_index].items.size(); i++) {
            if (sorted_bins[target_index].items[i].get_ItemSize() + sum_size <= current_size + sorted_bins[0].capacity_left) {
                target_items.push_back(sorted_bins[target_index].items[i]);     // remove the target item from current bin to temp items
                target_indexes.push_back(i);
                sum_size += sorted_bins[target_index].items[i].get_ItemSize();
                can_exchange1 = true;
            }
        }
        if (sum_size + sorted_bins[target_index].capacity_left >= current_size) {
            for (int i = 0; i < target_indexes.size(); i++) {
                sorted_bins[target_index].capacity_left += sorted_bins[target_index].items[target_indexes[i] - i].get_ItemSize();
                sorted_bins[target_index].items.erase(sorted_bins[target_index].items.begin() + target_indexes[i] - i);     // delete the target item from current bin
            }
            can_exchange2 = true;
        }
        if (can_exchange1 && can_exchange2) {
            // remove the current item from current bin to the target bin and delete the item from the current bin
            sorted_bins[target_index].items.push_back(sorted_bins[0].items[0]);
            sorted_bins[target_index].capacity_left -= current_size;
            sort(sorted_bins[target_index].items.rbegin(), sorted_bins[target_index].items.rend(), itemCmp); // keep the exchanged bin with sorted items.
            sorted_bins[0].capacity_left += current_size;
            sorted_bins[0].items.erase(sorted_bins[0].items.begin());
            // remove the target items from the temp items to the current bin
            for (int i = 0; i < target_items.size(); i++) {
                sorted_bins[0].items.push_back(target_items[i]);
                sorted_bins[0].capacity_left -= target_items[i].get_ItemSize();
            }
            sort(sorted_bins[0].items.rbegin(), sorted_bins[0].items.rend(),itemCmp);  // keep the exchanged bin with sorted items.
            flag = true;
        }
        solution.bins = sorted_bins;
        solution.objective = solution.bins.size();                
    }

    // Exchange randimBin with probability and reshuffle heuristic method
    // This heuristic randomly selects two non-fully-filled bins.
    // All items from these two bins are then considered and the best items’ combination is identified
    // so that it can maximally fill one bin. The remaining items are filled into the other bin.
    void Exchange_randomBin_Reshuffle(Solution &solution){

        emptybin_checker(solution);     // check the empty bin
        sort(solution.bins.rbegin(), solution.bins.rend(), binCmp);  // sort bins from big left capacity to small left capacity
        int exchangeBin_index1 = 0;
        int exchangeBin_index2 = 1;
        bool flag = false;     //valid exchangeBin_index1 and exchangeBin_index2
        //get the exchanged bin indexes
        int sum_capacity_left =0;
        for(int i=0; i<solution.bins.size(); i++){
            sum_capacity_left += solution.bins[i].capacity_left;
        }
        while(!flag) {
            int random_pointer1 = (rand() % sum_capacity_left) + 1;  // the random number is from 1 to sum_capacity_left
            int random_pointer2 = (rand() % sum_capacity_left) + 1;  // the random number is from 1 to sum_capacity_left
            for (int i = 0; i < solution.bins.size(); i++) {
                random_pointer1 -= solution.bins[i].capacity_left;
                if (random_pointer1 <= 0) {
                    exchangeBin_index1 = i;
                    break;
                }
            }
            for (int i = 0; i < solution.bins.size(); i++) {
                random_pointer2 -= solution.bins[i].capacity_left;
                if (random_pointer2 <= 0) {
                    exchangeBin_index2 = i;
                    break;
                }
            }
            if(exchangeBin_index1 != exchangeBin_index2){   // If the indexes of the two exchanged Bin are the same, randomly choose two again
                flag = true;
            }
        }

        // shuffle the items many times and get the best result which means maximally fill one bin
        int shuffle_count = 200;
        // store the whole items needed to be packed
        vector<Item> whole_items;
        for(int i=0; i<solution.bins[exchangeBin_index1].items.size(); i++){
            whole_items.push_back(solution.bins[exchangeBin_index1].items[i]);
        }
        for(int i=0; i<solution.bins[exchangeBin_index2].items.size(); i++){
            whole_items.push_back(solution.bins[exchangeBin_index2].items[i]);
        }
        // the best binpacking result of the two bins
        Bin best_exchangeBin1(solution.problem.bin_capacity);
        Bin best_exchangeBin2(solution.problem.bin_capacity);

        // obtain the best packing result
        for(int i=0; i<shuffle_count; i++){
            Bin exchangeBin1(solution.problem.bin_capacity);
            Bin exchangeBin2(solution.problem.bin_capacity);
            random_shuffle(whole_items.begin(), whole_items.end());
            for(int j=0; j<whole_items.size(); j++){
                if(whole_items[j].get_ItemSize()<=exchangeBin1.capacity_left){
                    exchangeBin1.items.push_back(whole_items[j]);
                    exchangeBin1.capacity_left -= whole_items[j].get_ItemSize();
                }else{
                    exchangeBin2.items.push_back(whole_items[j]);
                    exchangeBin2.capacity_left -= whole_items[j].get_ItemSize();
                }
            }
            if(exchangeBin1.capacity_left < best_exchangeBin1.capacity_left && exchangeBin1.capacity_left>=0 && exchangeBin2.capacity_left>=0 ){
                best_exchangeBin1 = exchangeBin1;
                best_exchangeBin2 = exchangeBin2;
            }
        }

        solution.bins[exchangeBin_index1] = best_exchangeBin1;
        solution.bins[exchangeBin_index2] = best_exchangeBin2;
    }

    // This function is used to generate an initial solution 
    // The initial solution first sort items from small size to large size and use first fit to pack them
    void Initial_Solution(Solution &solution){
        int bin_capacity = solution.problem.bin_capacity;
        bool flag_newBin = false;

        //This is for sorting items
        vector<Item> sorted_items;
        sorted_items = solution.problem.items;
        sort(sorted_items.begin(), sorted_items.end(), itemCmp);  // sort items from small-size to large-size
        
        Bin current_bin(bin_capacity);
        //First Fit
        current_bin.items.push_back(sorted_items[0]);
        current_bin.capacity_left = current_bin.capacity_left - sorted_items[0].get_ItemSize();
        solution.bins.push_back(current_bin);

        for(int i = 1; i<sorted_items.size(); i++){
            for(int k = 0; k<solution.bins.size(); k++){
                // Search the first fitted bin for this item
                if(sorted_items[i].get_ItemSize() < solution.bins[k].capacity_left){
                    solution.bins[k].items.push_back(sorted_items[i]);
                    solution.bins[k].capacity_left = solution.bins[k].capacity_left - sorted_items[i].get_ItemSize();
                    flag_newBin = false;
                    break;
                }
                flag_newBin = true;
            }
            if(flag_newBin){
                // If there is no fitted bin before, then push a new bin to take the item.
                Bin bin(bin_capacity);
                current_bin = bin;
                current_bin.items.push_back(sorted_items[i]);
                current_bin.capacity_left = current_bin.capacity_left - sorted_items[i].get_ItemSize();
                solution.bins.push_back(current_bin);
            }
        }

        solution.objective = solution.bins.size();
        solution.feasibility = solution.bins.size() - solution.problem.best_objective;
    }

    // This fuction is used for defining the variable neighbourhood spaces
    void Neighbourhood(int nb_space, Solution &solution){
        switch(nb_space)
        {
            case 1:{
                // 200 neighbourhood1 solutions space with LBLI, RandomBin_Reshuffule and shift heuristics
                int neighbour_count = 100;
                Solution local_best_solution = solution;
                for(int i =0; i<neighbour_count; i++){
                    Exchange_LBLI(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    if(local_best_solution.objective < solution.objective){
                        solution = local_best_solution;
                    }
                }
                break;
            }
            case 2:{
                // 200 neighbourhood2 solutions space with Split, LBLI and shift heuristics
                int neighbour_count = 100;
                Solution local_best_solution = solution;
                for(int i =0; i<neighbour_count; i++){
                    SplitStrategy(local_best_solution);
                    Exchange_LBLI(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    if(local_best_solution.objective < solution.objective){
                        solution = local_best_solution;
                    }
                }
                break;
            }
            case 3:{
                // 200 neighbourhood3 solutions space with hyprid heuristics
                int neighbour_count = 100;
                Solution local_best_solution = solution;
                for(int i =0; i<neighbour_count; i++){
                    Exchange_LBLI(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    SplitStrategy(local_best_solution);
                    Exchange_LBLI(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    SplitStrategy(local_best_solution);
                    Exchange_LBLI(local_best_solution);
                    Exchange_LBLI(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    Exchange_randomBin_Reshuffle(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    ShiftStrategy(local_best_solution);
                    if(local_best_solution.objective < solution.objective){
                        solution = local_best_solution;
                    }
                }
                break;
            }
            default:
                cout << "Bad nb_space!" << endl;
        }

    }

    // The function is used for shaking movement
    // This shaking movement uses exchange largestBin_largestItem heuristic method to shuffle two bins,
    // randomly reshuffle two random bin items and randomly exchange two items which are the largest item of each bin.
    void Shaking(Solution &solution){
        // reshuffle non-full bins
        vector<Bin>reshuffle_bins;
        vector<Bin>sorted_bins1 = solution.bins;
        vector<Item>reshuffle_items;
        sort(sorted_bins1.begin(), sorted_bins1.end(), binCmp);     // sort bins from small left capacity to big left capacity
        for(int i=0; i<sorted_bins1.size(); i++){
            if(sorted_bins1[i].capacity_left==0){
                reshuffle_bins.push_back(sorted_bins1[i]);
            }
            else{
                for(int j=0; j<sorted_bins1[i].items.size(); j++){
                    reshuffle_items.push_back(sorted_bins1[i].items[j]);
                }
            }
        }
        random_shuffle(reshuffle_items.begin(), reshuffle_items.end());

        int bin_capacity = solution.problem.bin_capacity;
        bool flag_newBin = false;

        Bin current_bin(bin_capacity);
        //First Fit
        current_bin.items.push_back(reshuffle_items[0]);
        current_bin.capacity_left = current_bin.capacity_left - reshuffle_items[0].get_ItemSize();
        reshuffle_bins.push_back(current_bin);

        for(int i = 1; i<reshuffle_items.size(); i++){
            for(int k = 0; k<reshuffle_bins.size(); k++){
                // Search the first fitted bin for this item
                if(reshuffle_items[i].get_ItemSize() < reshuffle_bins[k].capacity_left){
                    reshuffle_bins[k].items.push_back(reshuffle_items[i]);
                    reshuffle_bins[k].capacity_left = reshuffle_bins[k].capacity_left - reshuffle_items[i].get_ItemSize();
                    flag_newBin = false;
                    break;
                }
                flag_newBin = true;
            }
            if(flag_newBin){
                //If there is no fitted bin before, then push a new bin to take the item.
                Bin bin(bin_capacity);
                current_bin = bin;
                current_bin.items.push_back(reshuffle_items[i]);
                current_bin.capacity_left = current_bin.capacity_left - reshuffle_items[i].get_ItemSize();
                reshuffle_bins.push_back(current_bin);
            }
        }

        solution.bins = reshuffle_bins;

        // choose two bins randomly, reshuffle the items of them and pack them randomly
        int exchangeBin_index1 = rand()%solution.bins.size();
        int exchangeBin_index2 = rand()%solution.bins.size();
        vector<Bin> sorted_bins;
        emptybin_checker(solution);     // check the empty bin
        sorted_bins = solution.bins;
        sort(solution.bins.rbegin(), solution.bins.rend(), binCmp);  // sort bins from big left capacity to small left capacity

        // store the whole items needed to be packed
        vector<Item> whole_items;
        for(int i=0; i<solution.bins[exchangeBin_index1].items.size(); i++){
            whole_items.push_back(solution.bins[exchangeBin_index1].items[i]);
        }
        for(int i=0; i<solution.bins[exchangeBin_index2].items.size(); i++){
            whole_items.push_back(solution.bins[exchangeBin_index2].items[i]);
        }
        // check the random packing is valid
        bool flag_valid_randomPack = false;
        while(!flag_valid_randomPack) {
            Bin exchangeBin1(solution.problem.bin_capacity);
            Bin exchangeBin2(solution.problem.bin_capacity);
            random_shuffle(whole_items.begin(), whole_items.end());
            for (int j = 0; j < whole_items.size(); j++) {
                if (whole_items[j].get_ItemSize() <= exchangeBin1.capacity_left) {
                    exchangeBin1.items.push_back(whole_items[j]);
                    exchangeBin1.capacity_left -= whole_items[j].get_ItemSize();
                } else {
                    exchangeBin2.items.push_back(whole_items[j]);
                    exchangeBin2.capacity_left -= whole_items[j].get_ItemSize();
                }
            }
            if(exchangeBin1.capacity_left>=0 && exchangeBin2.capacity_left>=0){
                solution.bins[exchangeBin_index1] = exchangeBin1;
                solution.bins[exchangeBin_index2] = exchangeBin2;
                flag_valid_randomPack = true;
            }
        }

        // exchange randomly two items which is the largest item in each bin
        bool flag = true;
        while(flag){
            int exchangeBin_index1 = rand()%solution.bins.size();
            int exchangeBin_index2 = rand()%solution.bins.size();
            while(exchangeBin_index1 == exchangeBin_index2){
                exchangeBin_index2 = rand()%solution.bins.size();
            }

            bool can_exchange1 = (solution.bins[exchangeBin_index1].items[0].get_ItemSize() + solution.bins[exchangeBin_index1].capacity_left) > solution.bins[exchangeBin_index2].items[0].get_ItemSize();
            bool can_exchange2 = (solution.bins[exchangeBin_index2].items[0].get_ItemSize() + solution.bins[exchangeBin_index2].capacity_left) > solution.bins[exchangeBin_index1].items[0].get_ItemSize();
            if(can_exchange1 && can_exchange2){
                Item item1 = solution.bins[exchangeBin_index1].items[0];
                Item item2 = solution.bins[exchangeBin_index2].items[0];
                solution.bins[exchangeBin_index1].capacity_left += solution.bins[exchangeBin_index1].items[0].get_ItemSize();
                solution.bins[exchangeBin_index2].capacity_left += solution.bins[exchangeBin_index2].items[0].get_ItemSize();
                solution.bins[exchangeBin_index1].items.erase(solution.bins[exchangeBin_index1].items.begin());
                solution.bins[exchangeBin_index2].items.erase(solution.bins[exchangeBin_index2].items.begin());
                solution.bins[exchangeBin_index1].items.push_back(item2);                      //exchange item
                solution.bins[exchangeBin_index2].items.push_back(item1);
                solution.bins[exchangeBin_index1].capacity_left -= item2.get_ItemSize();      //update the capcity left of each bin
                solution.bins[exchangeBin_index2].capacity_left -= item1.get_ItemSize();
                sort(solution.bins[exchangeBin_index1].items.rbegin(), solution.bins[exchangeBin_index1].items.rend(), itemCmp);  // sort the exchaged items
                sort(solution.bins[exchangeBin_index2].items.rbegin(), solution.bins[exchangeBin_index2].items.rend(), itemCmp);

                flag = false;
            }
        }


    }

    // This fuction is used for variable neighbourhood search
    void Variable_Neighbourhood_Search(Problem problem){
        Solution current_solution;
        current_solution.problem = problem;
        Solution best_solution;

        clock_t time_start, time_fin;
        time_start = clock();
        double time_spent = 0;

        Initial_Solution(current_solution);
        best_solution = current_solution;

        while(time_spent < MAX_TIME)
        {
            //variable neighbourhood search
            int nb_space = 1;
            int maxSpace = 3;

            Solution n_best_solution;
            n_best_solution = current_solution;
        
            while(nb_space < maxSpace + 1)
            {
                Neighbourhood(nb_space, n_best_solution);

                if(n_best_solution.objective < current_solution.objective){
                    current_solution = n_best_solution;
                    nb_space = 1;
                }else{
                    nb_space ++;
                }

            }
            // One round variable neighbourhood search ends.

            // If the best solution is better than current one for each round, replace it.
            if(best_solution.objective > current_solution.objective)
            {
                best_solution = current_solution;
            }

            //If the solution get the best objective solution of the problem, finish this problem early
            if(best_solution.objective == best_solution.problem.best_objective ){
                time_fin = clock();
                time_spent = (double)(time_fin - time_start) / CLOCKS_PER_SEC;
                break;
            }

            Shaking(current_solution);


            time_fin = clock();
            time_spent = (double)(time_fin - time_start) / CLOCKS_PER_SEC;
        }
        my_solutions.push_back(best_solution);
    }

    // This function is used for outputing the solutions to the target file.
    void output_solutions(string data_file){
        ofstream outfile;
        outfile.open(data_file);
        if(! outfile.is_open()){
            cout << "Output file "+data_file+" does not exist. Please check!\n" << endl;
            exit(2);
        }

        //This is a test for output file
        outfile << problem_number << endl;
        for(int i=0; i < my_solutions.size(); i++){
            outfile << my_problems[i].name << endl;
            outfile << " obj=   ";
            outfile << my_solutions[i].bins.size();
            outfile << " ";
            outfile << my_solutions[i].bins.size()-my_solutions[i].problem.best_objective << endl;
            for(int j=0; j < my_solutions[i].bins.size(); j++){
                for(int k=0; k < my_solutions[i].bins[j].items.size(); k++){
                    outfile << my_solutions[i].bins[j].items[k].get_ItemIndex();
                    //outfile << my_solutions[i].bins[j].items[k].get_ItemSize();
                    outfile << " ";
                }
                outfile << endl;
            }
        }
        outfile.close();
    }

    // This is the getter for the vector with problems
    vector<Problem> get_problems(){
        return my_problems;
    }

private:
    vector<Problem> my_problems;     // vector to store problems
    vector<Solution> my_solutions;   // vector to store solutions
    int problem_number;
};


// This is the main function
int main(int argc, char * argv[]){
    string data_file;
    string solution_file;
    My_problems my_problems;
    srand((unsigned int)(time(NULL)));

    if(argc>7)
    {
        printf("Too many arguments.\n");
        return 1;
    }
    else if(argc!=7)
    {
        printf("Insufficient arguments. Please use the following options:\n   -s data_file (compulsory)\n   -o solution_file (compulsory)\n   -t max_time (in sec)\n");
        return 2;
    }
    else
    {
        for(int i=1; i<argc; i=i+2)
        {
            if(strcmp(argv[i], "-s") ==0)
                data_file = argv[i+1];
            else if(strcmp(argv[i], "-o") == 0)
                solution_file = argv[i+1];
            else if(strcmp(argv[i], "-t") == 0)
                MAX_TIME = stoi(argv[i+1]);
        }
    }

    my_problems.load_problems(data_file);   // load the file with problems

    for(int i = 0; i<my_problems.get_problems().size(); i++){
        my_problems.Variable_Neighbourhood_Search(my_problems.get_problems()[i]);    // Variable Neighbourhood Search
    }

    my_problems.output_solutions(solution_file);    // output the file with solutions

}