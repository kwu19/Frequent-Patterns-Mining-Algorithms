# -*- coding: utf-8 -*-
"""
author: @Kefei Wu
"""

from time import time

def create_C1(data_set):
    """
    Create frequent candidate 1-itemset C1.
    Input:
        data_set: a list of tuples contains attributes in each tuple.    
    Returns:
        C1: a set that contains frequent candidate 1-itemsets    
    """
    C1 = set()
    
    for i in data_set:
        for attr in i:
            attr_set = frozenset([attr])
            C1.add(attr_set)
    return C1


def satisfy_Lk(item_in_Ck, Lk_sub1):
    """
    Check whether this frequent candidate k-itemsets satisfy the apriori algorithm.    
    Input:
        Item_in_Ck: frequent candidate k-itemsets in all Ck 
        Lk_sub1: Lk-1 frequent k-1-itemsets
    Returns:
        True: satisfy Apriori property.
        False: does not satisfy Apriori property.
    """
    for attr in item_in_Ck:
        sub_Ck = item_in_Ck - frozenset([attr])
        if sub_Ck not in Lk_sub1:
            return False
    return True


def create_Ck(Lk_sub1, k):
    """
    Generate candidate k-itemsets Ck by Lk-1.
    Input:
        Lksub1: Lk-1 frequent k-1-itemsets 
        k: number of items in k-itemsets    
    Return:
        Ck: candidate k-itemsets.
    """
    Ck = set()
    _len = len(Lk_sub1)
    _list = list(Lk_sub1)
    
    for i in range(_len):
        for j in range(1, _len):
            l1 = list(_list[i])
            l2 = list(_list[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                item_in_Ck = _list[i] | _list[j]
                if satisfy_Lk(item_in_Ck, Lk_sub1): 
                    Ck.add(item_in_Ck) # add item to Ck if it satisfies apriori property
    return Ck


def generate_Lk(data_set, Ck, min_sup, sup_set):
    """
    Create frequent k-itemset Lk and calculate support for each frequent k-itemsets.
    Input:
        data_set: a list of tuples contains attributes in each tuple.
        Ck: candidates k-itemsets
        min_sup: minimum support that are given to it
        sup_set: a dictionary which key is frequent itemsets and the value is support. 
    Returns:
        Lk: a set that contains frequent k-itemsets    
    """
    Lk = set()
    _count = {}  # a dictionary which key is itemsets and value is frequency it appears
    
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in _count:
                    _count[item] = 1  
                else:
                    _count[item] += 1
                    
    t_num = float(len(data_set))
    for item in _count:
        if (_count[item] / t_num) >= min_sup:
            Lk.add(item)
            sup_set[item] = _count[item] / t_num  # calculate support
    return Lk


def generate_L(data_set, k, min_sup):
    """
    Generate all frequent itemsets.
    Input:
        data_set: a list of tuples contains attributes in each tuple.
        k: number of items in k-itemsets
        min_sup: minimum support that are given to it
    Returns:
        L: a list that contains all Lk we got        
        sup_set: a dictionary which key is frequent itemsets and the value is support.    
    """
    sup_set = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk(data_set, C1, min_sup, sup_set)
    Lk_sub1 = L1.copy()
    L = []
    L.append(Lk_sub1)
    
    for i in range(2, k+1):
        Ci = create_Ck(Lk_sub1, i)
        Li = generate_Lk(data_set, Ci, min_sup, sup_set)
        Lk_sub1 = Li.copy()
        L.append(Lk_sub1)
    return L, sup_set


def generate_association(L, sup_set, min_conf):
    """
    This method used to generate the association rules and confidence of each rule based on the frequent itemsets.
    Input:
        L: List of Lk.
        sup_set: a dictionary which key is frequent itemsets and the value is support.
        min_conf: the minimum confidence that are given to it
    Return:
        aso_rule_list: a list that contains all association rules
    """
    aso_rule_list = []
    sub_set_list = []
    
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = sup_set[freq_set] / sup_set[freq_set - sub_set]  # calculate confidence
                    aso_rule = (freq_set - sub_set, sub_set, conf)
                    if (conf >= min_conf and aso_rule not in aso_rule_list):
                        aso_rule_list.append(aso_rule)  # generate association rules
            sub_set_list.append(freq_set)
    return aso_rule_list


def upload_data():
    """
    This method is to read the UCI dataset as a list.
    Input: 
        None
    Return: 
        data_set: a list of tuples contains attributes in each tuple.   
    """
    with open('adult.data.txt') as inputfile:
        data_set = list()
        for line in inputfile.readlines():
            data_set.append(line.split(','))  
        return data_set


def apriori(data_set, min_sup):
    """
    This method is to implement the apriori algorithm to the dataset that we read.   
    Input: 
        data_set: a list of tuples contains attributes in each tuple.
        min_sup: minimum support
    Return: 
        L: List of Lk.
        sup_set: a dictionary which key is frequent itemsets and the value is support.
        association_rules: the rules for each frequent itemset in the format of A -> B.
    """
    k = len(data_set[0])
    L, sup_set = generate_L(data_set, k, min_sup)
    association_rules = generate_association(L, sup_set, min_conf = 0.7)
    display(L, sup_set, association_rules)
    return L, sup_set, association_rules


def display(L, sup_set, association_rules):
    """
    This method is to print the frequent patterns that the project got.
    Input: 
        L: List of Lk.
        sup_set: a dictionary which key is frequent itemsets and the value is support.
    Return: 
        None
    """
    i = 0
    while len(L[i]) != 0:
        i += 1
        for Lk in L[0:i]:
            print("="*50)
            print("frequent {}-itemsets".format(str(len(list(Lk)[0]))))
            for freq_set in Lk:
                print(freq_set)
                print("Support =" + str(sup_set[freq_set]))
    print("="*50)
    print("Association Rules Are As Follows:")
    for i in association_rules:
        print(str(list(i[0])) + "-->" + str(list(i[1])))
        print("Confidence = " + str(i[2]))


def main():
    min_support = 0.23
    data_set = upload_data()
    apriori(data_set, min_support)

if __name__ == "__main__":
    start = time()
    main()
    stop = time()
    print("Processing time is "+str(stop-start)+" seconds")
