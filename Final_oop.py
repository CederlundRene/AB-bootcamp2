import random
import pandas as pd
import numpy as np

# Definer organisation
# funktion sale_pr_day (input: #TiedAgent , #CustServiceRep, xx )
# funktion total_sale_month (input: sale_pr_day, month)

class Organisation:
    def __init__(self,org_name,num_cust=5, num_tiedA=5, num_days=30):
        self.org_name = org_name
        self.num_cust= num_cust
        self.num_tiedA= num_tiedA
        self.num_days = num_days

    def list_sales_person(self):
        org_salesp = SalesPerson(self.num_cust, self.num_tiedA)
        return org_salesp.new_sales_list

    def sale_pr_day(self,new_sales_list,dato=1):

        #Simuler liste with sales persons
        #new_sales_list = self.list_sales_person()
        #create df
        columns = ['name', 'department', 'hitrate', 'cost', 'leads_pr_day', 'leadnr', 'converted', 'leadcost', 'sales']
        df_sales = pd.DataFrame(columns=columns)

        for item in new_sales_list:
            dict_sales= {}
            dict_sales.update(item)
            for i in range(1, item['leads_pr_day'] + 1, 1):
                dict_sales['leadnr'] = i

                # simuler new lead
                leads = Lead()
                newlead = leads.new_lead()

                # simuler om lead convert to sale
                y = random.uniform(0, 1)
                converted = (dict_sales["hitrate"] >= y)
                dict_sales['converted'] = converted
                dict_sales['leadcost'] = newlead['lead_cost']

                if converted == True:
                    dict_sales['sales'] = newlead['potential_sale']
                else:
                    dict_sales['sales'] = 0
                #print(dict_sales)
                df_sales = df_sales.append(dict_sales, ignore_index=True)


        dict_total_sales_day = df_sales[['cost','leadcost','sales']].aggregate(np.sum).to_dict()
        dict_total_sales_day['converted_leads'] = df_sales[df_sales['converted'] == True]['leadnr'].count()
        dict_total_sales_day['leads']= df_sales['leadnr'].count()
        dict_total_sales_day['CustServiceRep'] = self.num_cust
        dict_total_sales_day['tiedAgent'] = self.num_tiedA
        dict_total_sales_day['leads'] = df_sales['leadnr'].count()
        print(f"Lead list day {dato} with {len(df_sales)} lead is generated")
        #return df_sales[['cost','leadcost','sales']].aggregate(np.sum).to_dict()
        return dict_total_sales_day

    def total_sale_month(self):
        #step 1: simuler salesperson list
        new_sales_list = self.list_sales_person()
        #step 2: tom dict
        columns = ['day', 'cost', 'leadcost', 'sales','converted_leads','leads','CustServiceRep','tiedAgent']
        df_sales_month = pd.DataFrame(columns=columns)
        for i in range(1,self.num_days+1,1):
            #print(i)
            dict_sales_month   = {}
            dict_sales_month    = self.sale_pr_day(new_sales_list,dato= i)
            dict_sales_month['day'] = 'day ' + str(i)
            df_sales_month = df_sales_month.append(dict_sales_month , ignore_index=True)
        #print(f"New list with {len(df_sales_month)} days of sales simulated")
        print(f"--------------------------------------------------------")
        print(f"Simulated - Sales rapport 30 days - {self.org_name}")
        print(f"--------------------------------------------------------")
        print(f"Number of CustServiceRep =  {df_sales_month['CustServiceRep'].max()} ")
        print(f"Number of tiedAgent =  {df_sales_month['tiedAgent'].max()} ")
        print(f"--------------------------------------------------------")
        print(f"Number of conversions =  {df_sales_month['converted_leads'].sum()} leads")
        print(f"Number of leads =        {df_sales_month['leads'].sum()} leads")
        print("Conversionrate = " + "         {:.2%}".format(df_sales_month['converted_leads'].sum() / (70 * 30)))
        print(f"--------------------------------------------------------")
        print(f"Total sales =            {df_sales_month['sales'].sum()} in dkr")
        print(f"Total employee cost =    {df_sales_month['cost'].sum()} in dkr")
        print(f"Total lead cost =        {df_sales_month['leadcost'].sum()} in dkr")
        print(
            f"Gross profit =           {df_sales_month['sales'].sum() - df_sales_month['cost'].sum() - df_sales_month['leadcost'].sum()} in dkr")
        print(f"--------------------------------------------------------")
        print(f"Minimum daily sales =    {df_sales_month['sales'].min()} in dkr")
        print(f"Maximum daily sales =    {df_sales_month['sales'].max()} in dkr")
        print(f"Mean daily sales =        {round(df_sales_month['sales'].mean(), 0)} in dkr")
        print(f"Std daily sales =        {round(df_sales_month['sales'].std(), 0)} in dkr")
        print(f"--------------------------------------------------------")
        return df_sales_month

# Definer en salesPerson som klasse
# funktion sum_converted (sale_pr_day)

class SalesPerson:

    def __init__(self,num_Cust, num_tiedA):
        self.num_Cust = num_Cust
        self.num_tiedA = num_tiedA

    @property
    def new_sales_list(self):
        new_sales_persons = []

        for x in range(1, self.num_Cust + 1, 1):
            custsevicename = CustServiceResp(name='C_' + str(x))
            new_sales_persons.append(custsevicename.all())

        for y in range(1, self.num_tiedA + 1, 1):
            tname = TiedAgent(name='t_' + str(y))
            new_sales_persons.append(tname.all())

        print(f"New list with {len(new_sales_persons)} sales person generated")
        return (new_sales_persons)

# Class TiedAgent
class TiedAgent(SalesPerson):

    def __init__(self, name="test",department="TiedAgent", hitrate=0.4,cost=1000,leads_pr_day=4):
        self.name = name
        self.department = department
        self.hitrate = hitrate
        self.cost = cost
        self.leads_pr_day = leads_pr_day

    def all(self):
        return {'name': self.name, 'department': self.department, 'hitrate': self.hitrate, 'cost': self.cost,
                 'leads_pr_day': self.leads_pr_day}

# Class CustServiceResp
class CustServiceResp():

    def __init__(self, name="test",department="CustServiceResp", hitrate=0.2,cost=300,leads_pr_day=10):
        #super().__init__("test", "CustServiceResp")
        self.name=name
        self.department=department
        self.hitrate = hitrate
        self.cost = cost
        self.leads_pr_day = leads_pr_day

     def all(self):
      return {'name':self.name,'department':self.department,'hitrate':self.hitrate ,'cost':self.cost ,'leads_pr_day':self.leads_pr_day}


# Class lead
class Lead:

    def __init__(self,lead_cost=25):
        self.lead_cost =lead_cost
        self.converted_to_sale = False
        self.potential_sale = round(random.uniform(1000,10000))

    def __repr__(self):
        return f"Potential sale ={self.potential_sale} lead cost = {self.lead_cost}"

    def new_lead(self):
        return {'potential_sale':self.potential_sale,'lead_cost':self.lead_cost}

x = Lead()
print(x.new_lead())


# Run list of sales person
# Run list of sales pr day
# Run list of sales pr month

##########################################################
#                    Test simulation                     #
##########################################################

# sales report
ab = Organisation('AB',num_cust=5, num_tiedA=5, num_days = 30 )
d_month =ab.total_sale_month()
d_month


# list with sales person
list = ab.list_sales_person()
print(list)


# list with daily sales (lead)
d_day=ab.sale_pr_day(list)
d_day

# generate lead
x = Lead()
print(x.new_lead())

