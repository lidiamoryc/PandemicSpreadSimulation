import numpy as np

def age_infection_proba(age):
    interim_val = 0.03 * age - 5
    return 1.0 / (1 + np.exp(-(interim_val)))

def gender_infection_proba(gender):
    return 0.0 if gender == 'Male' else 0.01

def vaccinated_infection_proba(vaccinated):
    return -0.11 if vaccinated == 'True' else 0

def mask_infection_proba(mask):
    return -0.07 if mask == 'True' else 0

def age_recovery_proba(age):
    interim_val = 0.02 * age - 3
    return -1.0 / (1 + np.exp(-(interim_val)))

def gender_recovery_proba(gender):
    return 0.0 if gender == 'Male' else -0.01

def vaccinated_recovery_proba(vaccinated):
    return 0

def mask_recovery_proba(mask):
    return 0

def age_mortality_proba(age):
    return 0.1 / (1 + np.exp(-0.02 * (age - 40))) 

def gender_mortality_proba(gender):
    return 0.002 if gender == 'Male' else 0.001

def vaccinated_mortality_proba(vaccinated):
    return -0.03 if vaccinated == 'True' else 0

def mask_mortality_proba(mask):
    return 0

def age_immunity_loss_proba(age):
    return (age - 30) * 0.001 + 0.05

def gender_immunity_loss_proba(gender):
    return 0.02 if gender == 'Male' else 0.01

def vaccinated_immunity_loss_proba(vaccinated):
    return -0.15 if vaccinated == 'True' else 0

def mask_immunity_loss_proba(mask):
    return 0