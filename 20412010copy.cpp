
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
    Item(int weight, int id){
        item_weight = weight;
        item_id = id;
    }
    // This function is the getter of item_weight
    int get_ItemWeight(){
        return item_weight;
    }
    // This funciton is the gettrt of item_id
    int get_ItemID(){
        return item_id;
    }
private:
    int item_weight;
    int item_id;
};

// This class is about a bin to contain items
class Bin{
public:
    int cap_left;
    vector<Item> items;

    // Constructor of Bin
    Bin(int capacity){
        cap_left = capacity;
    }
};

// This class is about a problem to be solved
class Problem{
public:
    vector<Item> items;
    string name;
    int item_number;
    int bin_capacity;
    float best_bins_number;
};

// This class is about a solution for a problem
class Solution{
public: 
    Problem problem;
    float bins_number;
    vector<Bin> bins;

};

// This class is about mainly solving problems using VNS
class bin_packing_problem{
public: 
    // This function is used for initializing all the problems
    void initial_problems(int problem_number){
        for(int i=0; i<problem_number; i++){
            Problem problem;
            bin_packing_problem.push_back(problem);
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
            bin_packing_problem[i].name = str_temp;

            openfile >> temp;
            bin_packing_problem[i].bin_capacity = temp;

            openfile >> temp;
            bin_packing_problem[i].item_number = temp;
    
            openfile >> temp;
            bin_packing_problem[i].best_bins_number = temp;

            for(int j=0; j<bin_packing_problem[i].item_number; j++){
                openfile >> temp;
                Item item(temp, j);
                bin_packing_problem[i].items.push_back(item);
            }
        }
        openfile.close();
    }

    static bool itemCmp(Item item1, Item item2){
        if(item1.get_ItemWeight()>item2.get_ItemWeight())
        {
            return true;
        }
        else{
            return false;
        }
    }
    void emptybin_check(Solution &solution){
        for(int i=0; i<solution.bins.size(); i++){
            if(solution.bins[i].items.size()== 0){
                solution.bins.erase(solution.bins.begin()+i);
                i--;
            }
        }
    }
    static bool binCmp(Bin bin1, Bin bin2){
        if(bin1.cap_left < bin2.cap_left)
        {
            return true;
        }
        else{
            return false;
        }
    }


    void Getsmallitems(Solution &solution){
        int avg_number = solution.problem.item_number/solution.bins.size();   // average item numbers per bin
        int place_split;  
        for(int i=0; i<solution.bins.size(); i++){
            if(solution.bins[i].items.size() > avg_number){
                place_split = solution.bins[i].items.size()/2;
                random_shuffle(solution.bins[i].items.begin(), solution.bins[i].items.end());   // shuffle the items which will be repacked
                Bin bin(solution.problem.bin_capacity);
                for(int j=0; j<place_split; j++){
                    bin.items.push_back(solution.bins[i].items[j]);     // move the item from the current bin to a new bin
                    solution.bins[i].cap_left += solution.bins[i].items[j].get_ItemWeight();
                    bin.cap_left -= solution.bins[i].items[j].get_ItemWeight();
                }
                solution.bins[i].items.erase(solution.bins[i].items.begin(), solution.bins[i].items.begin()+place_split); // delete the chosen items from the current bin
                sort(bin.items.rbegin(), bin.items.rend(), itemCmp);    // sort the
                sort(solution.bins[i].items.rbegin(), solution.bins[i].items.rend(), itemCmp);
                solution.bins.push_back(bin);
                break;
            }
        }
        solution.bins_number = solution.bins.size();
    }

    // change largestBin_largestItem heuristic method
    // change the largest item in the largest left capacity bin with the items which are in a radom bin and can be changed into the current bin
    void Getbigcapleftbins(Solution &solution){
        emptybin_check(solution); // check the empty bin
        bool flag = false;       //successfully changed flag
        vector<Bin> sortedBins;
        sortedBins = solution.bins;
        sort(sortedBins.rbegin(), sortedBins.rend(), binCmp);  // sort bins from big left capacity to small left capacity
        // record all the ides of the bin which is not full
        vector<int> nofull_bin;
        for(int i=1; i<sortedBins.size(); i++)
        {
            if(sortedBins[i].cap_left>0){
                nofull_bin.push_back(i);
            }
        }
        int target_bin = nofull_bin[rand() % nofull_bin.size()]; // get the id of a random bin which is not full
        vector<Item> target_items;      // a temporary items to store the items will be changed
        vector<int> target_bins;
        // Because the bins and items of each bin have been sorted from big one to small one,
        // the largest item from the bin with the largest residual capacity is the first item of the first bins.
        bool can_fit1 = false;
        bool can_fit2 = false;
        sort(sortedBins[0].items.rbegin(), sortedBins[0].items.rend(), itemCmp);  // sort the items from large one to small one in the bin with the largest left capacity
        int current_weight = sortedBins[0].items[0].get_ItemWeight();
        int sum_weight = 0;     //sum of the size of the target items
        for (int i = 0; i < sortedBins[target_bin].items.size(); i++) {
            if (sortedBins[target_bin].items[i].get_ItemWeight() + sum_weight <= current_weight + sortedBins[0].cap_left) {
                target_items.push_back(sortedBins[target_bin].items[i]);     // remove the target item from current bin to temp items
                target_bins.push_back(i);
                sum_weight += sortedBins[target_bin].items[i].get_ItemWeight();
                can_fit1 = true;
            }
        }
        if (sum_weight + sortedBins[target_bin].cap_left >= current_weight) {
            for (int i = 0; i < target_bins.size(); i++) {
                sortedBins[target_bin].cap_left += sortedBins[target_bin].items[target_bins[i] - i].get_ItemWeight();
                sortedBins[target_bin].items.erase(sortedBins[target_bin].items.begin() + target_bins[i] - i);     // delete the target item from current bin
            }
            can_fit2 = true;
        }
        if (can_fit1 && can_fit2) {
            // remove the current item from current bin to the target bin and delete the item from the current bin
            sortedBins[target_bin].items.push_back(sortedBins[0].items[0]);
            sortedBins[target_bin].cap_left -= current_weight;
            sort(sortedBins[target_bin].items.rbegin(), sortedBins[target_bin].items.rend(), itemCmp); // keep the changed bin with sorted items.
            sortedBins[0].cap_left += current_weight;
            sortedBins[0].items.erase(sortedBins[0].items.begin());
            // remove the target items from the temp items to the current bin
            for (int i = 0; i < target_items.size(); i++) {
                sortedBins[0].items.push_back(target_items[i]);
                sortedBins[0].cap_left -= target_items[i].get_ItemWeight();
            }
            sort(sortedBins[0].items.rbegin(), sortedBins[0].items.rend(),itemCmp);  // keep the changed bin with sorted items.
            flag = true;
        }
        solution.bins = sortedBins;
        solution.bins_number = solution.bins.size();                
    }

    // change randimBin with probability and reshuffle heuristic method
    // This heuristic randomly selects two non-fully-filled bins.
    // All items from these two bins are then considered and the best items’ combination is identified
    // so that it can maximally fill one bin. The remaining items are filled into the other bin.
    void Randombin_Best_Fit(Solution &solution){

        emptybin_check(solution);     // check the empty bin
        sort(solution.bins.rbegin(), solution.bins.rend(), binCmp);  // sort bins from big left capacity to small left capacity
        int changeBin_id1 = 0;
        int changeBin_id2 = 1;
        bool flag = false;     //valid changeBin_id1 and changeBin_id2
        //get the changed bin ides
        int sum_cap_left =0;
        for(int i=0; i<solution.bins.size(); i++){
            sum_cap_left += solution.bins[i].cap_left;
        }
        while(!flag) {
            int random_pointer1 = (rand() % sum_cap_left) + 1;  // the random number is from 1 to sum_cap_left
            int random_pointer2 = (rand() % sum_cap_left) + 1;  // the random number is from 1 to sum_cap_left
            for (int i = 0; i < solution.bins.size(); i++) {
                random_pointer1 -= solution.bins[i].cap_left;
                if (random_pointer1 <= 0) {
                    changeBin_id1 = i;
                    break;
                }
            }
            for (int i = 0; i < solution.bins.size(); i++) {
                random_pointer2 -= solution.bins[i].cap_left;
                if (random_pointer2 <= 0) {
                    changeBin_id2 = i;
                    break;
                }
            }
            if(changeBin_id1 != changeBin_id2){   // If the ides of the two changed Bin are the same, randomly choose two again
                flag = true;
            }
        }

        // shuffle the items many times and get the best result which means maximally fill one bin
        int randomNumber = 200;
        // store the whole items needed to be packed
        vector<Item> whole_items;
        for(int i=0; i<solution.bins[changeBin_id1].items.size(); i++){
            whole_items.push_back(solution.bins[changeBin_id1].items[i]);
        }
        for(int i=0; i<solution.bins[changeBin_id2].items.size(); i++){
            whole_items.push_back(solution.bins[changeBin_id2].items[i]);
        }
        // the best binpacking result of the two bins
        Bin best_changeBin1(solution.problem.bin_capacity);
        Bin best_changeBin2(solution.problem.bin_capacity);

        // obtain the best packing result
        for(int i=0; i<randomNumber; i++){
            Bin changeBin1(solution.problem.bin_capacity);
            Bin changeBin2(solution.problem.bin_capacity);
            random_shuffle(whole_items.begin(), whole_items.end());
            for(int j=0; j<whole_items.size(); j++){
                if(whole_items[j].get_ItemWeight()<=changeBin1.cap_left){
                    changeBin1.items.push_back(whole_items[j]);
                    changeBin1.cap_left -= whole_items[j].get_ItemWeight();
                }else{
                    changeBin2.items.push_back(whole_items[j]);
                    changeBin2.cap_left -= whole_items[j].get_ItemWeight();
                }
            }
            if(changeBin1.cap_left < best_changeBin1.cap_left && changeBin1.cap_left>=0 && changeBin2.cap_left>=0 ){
                best_changeBin1 = changeBin1;
                best_changeBin2 = changeBin2;
            }
        }

        solution.bins[changeBin_id1] = best_changeBin1;
        solution.bins[changeBin_id2] = best_changeBin2;
    }
    void Fit_Again(Solution &solution){
        vector<Bin> sortedBins;
        sortedBins = solution.bins;
        sort(sortedBins.begin(), sortedBins.end(), binCmp);  // sort bins from small left capacity to big left capacity
        //best fit
        for(int i = 0; i < sortedBins.back().items.size(); i++)
        {
            for(int j = 0; j < sortedBins.size()-1; j++)  // look for the target bin with the smallest capacity that fits the item
            {
                if(sortedBins.back().items[i].get_ItemWeight() <= sortedBins[j].cap_left)
                {
                    sortedBins[j].items.push_back(sortedBins.back().items[i]);    // shift the item to the target bin
                    sortedBins[j].cap_left -= sortedBins.back().items[i].get_ItemWeight();
                    sort(sortedBins[j].items.rbegin(), sortedBins[j].items.rend(), itemCmp);    // sort the bin with shifted item from big size to small size
                    sortedBins.back().cap_left += sortedBins.back().items[i].get_ItemWeight();
                    sortedBins.back().items.erase(sortedBins.back().items.begin()+i);     // delete the item from the original bin
                    i--;    // because of the deletion of the item, the id back to the previous one
                    if(sortedBins.back().items.size()==0)
                    {
                        sortedBins.pop_back();
                    }
                    break;
                }
            }
        }
        solution.bins = sortedBins;
        solution.bins_number = solution.bins.size(); 
        emptybin_check(solution);   //check the empty bin
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
        current_bin.cap_left = current_bin.cap_left - sorted_items[0].get_ItemWeight();
        solution.bins.push_back(current_bin);

        for(int i = 1; i<sorted_items.size(); i++){
            for(int k = 0; k<solution.bins.size(); k++){
                // Search the first fitted bin for this item
                if(sorted_items[i].get_ItemWeight() < solution.bins[k].cap_left){
                    solution.bins[k].items.push_back(sorted_items[i]);
                    solution.bins[k].cap_left = solution.bins[k].cap_left - sorted_items[i].get_ItemWeight();
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
                current_bin.cap_left = current_bin.cap_left - sorted_items[i].get_ItemWeight();
                solution.bins.push_back(current_bin);
            }
        }

        solution.bins_number = solution.bins.size();
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
                    Getbigcapleftbins(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    if(local_best_solution.bins_number < solution.bins_number){
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
                    Getsmallitems(local_best_solution);
                    Getbigcapleftbins(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    if(local_best_solution.bins_number < solution.bins_number){
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
                    Getbigcapleftbins(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Getsmallitems(local_best_solution);
                    Getbigcapleftbins(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Getsmallitems(local_best_solution);
                    Getbigcapleftbins(local_best_solution);
                    Getbigcapleftbins(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Randombin_Best_Fit(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    Fit_Again(local_best_solution);
                    if(local_best_solution.bins_number < solution.bins_number){
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
    // This shaking movement uses change largestBin_largestItem heuristic method to shuffle two bins,
    // randomly reshuffle two random bin items and randomly change two items which are the largest item of each bin.
    void Shaking(Solution &solution){
        // reshuffle non-full bins
        vector<Bin>reshuffle_bins;
        vector<Bin>sortedBins1 = solution.bins;
        vector<Item>reshuffle_items;
        sort(sortedBins1.begin(), sortedBins1.end(), binCmp);     // sort bins from small left capacity to big left capacity
        for(int i=0; i<sortedBins1.size(); i++){
            if(sortedBins1[i].cap_left==0){
                reshuffle_bins.push_back(sortedBins1[i]);
            }
            else{
                for(int j=0; j<sortedBins1[i].items.size(); j++){
                    reshuffle_items.push_back(sortedBins1[i].items[j]);
                }
            }
        }
        random_shuffle(reshuffle_items.begin(), reshuffle_items.end());

        int bin_capacity = solution.problem.bin_capacity;
        bool flag_newBin = false;

        Bin current_bin(bin_capacity);
        //First Fit
        current_bin.items.push_back(reshuffle_items[0]);
        current_bin.cap_left = current_bin.cap_left - reshuffle_items[0].get_ItemWeight();
        reshuffle_bins.push_back(current_bin);

        for(int i = 1; i<reshuffle_items.size(); i++){
            for(int k = 0; k<reshuffle_bins.size(); k++){
                // Search the first fitted bin for this item
                if(reshuffle_items[i].get_ItemWeight() < reshuffle_bins[k].cap_left){
                    reshuffle_bins[k].items.push_back(reshuffle_items[i]);
                    reshuffle_bins[k].cap_left = reshuffle_bins[k].cap_left - reshuffle_items[i].get_ItemWeight();
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
                current_bin.cap_left = current_bin.cap_left - reshuffle_items[i].get_ItemWeight();
                reshuffle_bins.push_back(current_bin);
            }
        }

        solution.bins = reshuffle_bins;

        // choose two bins randomly, reshuffle the items of them and pack them randomly
        int changeBin_id1 = rand()%solution.bins.size();
        int changeBin_id2 = rand()%solution.bins.size();
        vector<Bin> sortedBins;
        emptybin_check(solution);     // check the empty bin
        sortedBins = solution.bins;
        sort(solution.bins.rbegin(), solution.bins.rend(), binCmp);  // sort bins from big left capacity to small left capacity

        // store the whole items needed to be packed
        vector<Item> whole_items;
        for(int i=0; i<solution.bins[changeBin_id1].items.size(); i++){
            whole_items.push_back(solution.bins[changeBin_id1].items[i]);
        }
        for(int i=0; i<solution.bins[changeBin_id2].items.size(); i++){
            whole_items.push_back(solution.bins[changeBin_id2].items[i]);
        }
        // check the random packing is valid
        bool flag_valid_randomPack = false;
        while(!flag_valid_randomPack) {
            Bin changeBin1(solution.problem.bin_capacity);
            Bin changeBin2(solution.problem.bin_capacity);
            random_shuffle(whole_items.begin(), whole_items.end());
            for (int j = 0; j < whole_items.size(); j++) {
                if (whole_items[j].get_ItemWeight() <= changeBin1.cap_left) {
                    changeBin1.items.push_back(whole_items[j]);
                    changeBin1.cap_left -= whole_items[j].get_ItemWeight();
                } else {
                    changeBin2.items.push_back(whole_items[j]);
                    changeBin2.cap_left -= whole_items[j].get_ItemWeight();
                }
            }
            if(changeBin1.cap_left>=0 && changeBin2.cap_left>=0){
                solution.bins[changeBin_id1] = changeBin1;
                solution.bins[changeBin_id2] = changeBin2;
                flag_valid_randomPack = true;
            }
        }

        // change randomly two items which is the largest item in each bin
        bool flag = true;
        while(flag){
            int changeBin_id1 = rand()%solution.bins.size();
            int changeBin_id2 = rand()%solution.bins.size();
            while(changeBin_id1 == changeBin_id2){
                changeBin_id2 = rand()%solution.bins.size();
            }

            bool can_fit1 = (solution.bins[changeBin_id1].items[0].get_ItemWeight() + solution.bins[changeBin_id1].cap_left) > solution.bins[changeBin_id2].items[0].get_ItemWeight();
            bool can_fit2 = (solution.bins[changeBin_id2].items[0].get_ItemWeight() + solution.bins[changeBin_id2].cap_left) > solution.bins[changeBin_id1].items[0].get_ItemWeight();
            if(can_fit1 && can_fit2){
                Item item1 = solution.bins[changeBin_id1].items[0];
                Item item2 = solution.bins[changeBin_id2].items[0];
                solution.bins[changeBin_id1].cap_left += solution.bins[changeBin_id1].items[0].get_ItemWeight();
                solution.bins[changeBin_id2].cap_left += solution.bins[changeBin_id2].items[0].get_ItemWeight();
                solution.bins[changeBin_id1].items.erase(solution.bins[changeBin_id1].items.begin());
                solution.bins[changeBin_id2].items.erase(solution.bins[changeBin_id2].items.begin());
                solution.bins[changeBin_id1].items.push_back(item2);                      //change item
                solution.bins[changeBin_id2].items.push_back(item1);
                solution.bins[changeBin_id1].cap_left -= item2.get_ItemWeight();      //update the capcity left of each bin
                solution.bins[changeBin_id2].cap_left -= item1.get_ItemWeight();
                sort(solution.bins[changeBin_id1].items.rbegin(), solution.bins[changeBin_id1].items.rend(), itemCmp);  // sort the exchaged items
                sort(solution.bins[changeBin_id2].items.rbegin(), solution.bins[changeBin_id2].items.rend(), itemCmp);

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

                if(n_best_solution.bins_number < current_solution.bins_number){
                    current_solution = n_best_solution;
                    nb_space = 1;
                }else{
                    nb_space ++;
                }

            }
            // One round variable neighbourhood search ends.

            // If the best solution is better than current one for each round, replace it.
            if(best_solution.bins_number > current_solution.bins_number)
            {
                best_solution = current_solution;
            }

            //If the solution get the best bins_number solution of the problem, finish this problem early
            if(best_solution.bins_number == best_solution.problem.best_bins_number ){
                time_fin = clock();
                time_spent = (double)(time_fin - time_start) / CLOCKS_PER_SEC;
                break;
            }

            Shaking(current_solution);


            time_fin = clock();
            time_spent = (double)(time_fin - time_start) / CLOCKS_PER_SEC;
        }
        good_solutions.push_back(best_solution);
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
        for(int i=0; i < good_solutions.size(); i++){
            outfile << bin_packing_problem[i].name << endl;
            outfile << " obj=   ";
            outfile << good_solutions[i].bins.size();
            outfile << " ";
            outfile << good_solutions[i].bins.size()-good_solutions[i].problem.best_bins_number << endl;
            for(int j=0; j < good_solutions[i].bins.size(); j++){
                for(int k=0; k < good_solutions[i].bins[j].items.size(); k++){
                    outfile << good_solutions[i].bins[j].items[k].get_ItemID();
                    //outfile << good_solutions[i].bins[j].items[k].get_ItemWeight();
                    outfile << " ";
                }
                outfile << endl;
            }
        }
        outfile.close();
    }

    // This is the getter for the vector with problems
    vector<Problem> get_problems(){
        return bin_packing_problem;
    }

private:
    vector<Problem> bin_packing_problem;     // vector to store problems
    vector<Solution> good_solutions;   // vector to store solutions
    int problem_number;
};


// This is the main function
int main(int argc, char * argv[]){
    string data_file;
    string solution_file;
    bin_packing_problem bin_packing_problem;
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

    bin_packing_problem.load_problems(data_file);   // load the file with problems

    for(int i = 0; i<bin_packing_problem.get_problems().size(); i++){
        bin_packing_problem.Variable_Neighbourhood_Search(bin_packing_problem.get_problems()[i]);    // Variable Neighbourhood Search
    }

    bin_packing_problem.output_solutions(solution_file);    // output the file with solutions

}