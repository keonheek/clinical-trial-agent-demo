window.TRACES = [
  {
    "patient_id": "S001",
    "patient_text": "A 54-year-old man with a history of chronic alcohol use presents with severe epigastric pain radiating to the back, nausea, and vomiting. Labs reveal markedly elevated serum lipase and amylase.",
    "extraction": [
      {
        "name": "Age",
        "value": "54 years old",
        "evidence_quote": "A 54-year-old man"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "A 54-year-old man"
      },
      {
        "name": "Chief Complaint/Primary Symptom",
        "value": "Severe epigastric pain radiating to the back",
        "evidence_quote": "severe epigastric pain radiating to the back"
      },
      {
        "name": "Associated Symptoms",
        "value": "Nausea and vomiting",
        "evidence_quote": "nausea, and vomiting"
      },
      {
        "name": "Medical History",
        "value": "Chronic alcohol use",
        "evidence_quote": "history of chronic alcohol use"
      },
      {
        "name": "Serum Lipase",
        "value": "Markedly elevated",
        "evidence_quote": "markedly elevated serum lipase"
      },
      {
        "name": "Serum Amylase",
        "value": "Markedly elevated",
        "evidence_quote": "markedly elevated serum lipase and amylase"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06179459",
        "title": "Registry of Patients Undergoing Endoscopic Management of Pancreatic Fluid Collections",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 54 years old",
            "reasoning": "Patient is 54 years old, which meets the criterion of age ≥ 18 years."
          },
          {
            "text": "All patients undergoing endoscopic treatment of pancreatic fluid collections",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette describes acute pancreatitis presentation but contains no information about endoscopic treatment or pancreatic fluid collections."
          },
          {
            "text": "Age < 18 years",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Age: 54 years old",
            "reasoning": "Patient is 54 years old; the exclusion criterion (age < 18) does not apply to this patient."
          },
          {
            "text": "Patients who did not receive endoscopic treatment of pancreatic fluid collections",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not specify whether endoscopic treatment was received or planned."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Acute pancreatitis with elevated lipase/amylase confirmed; eligibility depends on whether endoscopic pancreatic fluid collection management is clinically indicated—currently unknown."
      },
      {
        "nct_id": "NCT06401577",
        "title": "Diabetes RElated to Acute Pancreatitis and Its Mechanisms: Metabolic Outcomes Using Novel CGM Metrics",
        "phase": "NA",
        "criteria": [
          {
            "text": "Diagnosis of acute pancreatitis (AP) 0-90 days prior to enrollment",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Severe epigastric pain radiating to the back, markedly elevated serum lipase and amylase, consistent with acute pancreatitis presentation",
            "reasoning": "Clinical presentation and markedly elevated pancreatic enzymes diagnostic of acute pancreatitis"
          },
          {
            "text": "Participant fully understands and is able to participate in all aspects of the study, including providing informed consent, completion of case report forms, telephone interviews, metabolic testing, and planned longitudinal follow-ups",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's understanding, capacity for informed consent, or ability to participate"
          },
          {
            "text": "Diagnosis of definite chronic pancreatitis (CP) at enrollment based on parenchymal or ductal calcifications on CT scan, or intraductal filling defects suggestive of calcifications on MRI and/or MRCP",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No imaging findings (CT, MRI, MRCP) reported; cannot assess for calcifications or parenchymal changes"
          },
          {
            "text": "Post-endoscopic retrograde cholangiopancreatography (ERCP) acute pancreatitis with hospitalization for less than 48 hours",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of ERCP procedure or hospitalization duration; cannot determine if criterion applies"
          },
          {
            "text": "Prior direct endoscopic necrosectomy of the pancreas or percutaneous necrosectomy or drainage of necrotic collection(s) before enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior surgical history documented regarding endoscopic or percutaneous necrosectomy"
          },
          {
            "text": "Pancreatic tumors, including ductal adenocarcinoma, neuroendocrine tumors, and metastasis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No imaging or tumor screening results provided; pancreatic malignancy not addressed"
          },
          {
            "text": "Confirmed or suspected cystic tumor associated with main pancreatic duct dilation, or believed to be the cause of acute pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No imaging findings reported regarding cystic tumors or pancreatic duct dilation"
          },
          {
            "text": "Prior pancreatic surgery, including distal pancreatectomy, pancreaticoduodenectomy, pancreatic necrosectomy, or Frey procedure",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior pancreatic surgical history documented in available information"
          },
          {
            "text": "Use of disallowed concomitant medications within 30 days prior to enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Medications used in past 30 days not specified; trial's disallowed medication list unknown"
          },
          {
            "text": "History of solid organ transplant, acquired immunodeficiency syndrome (AIDS), active treatment for cancer (except non-melanoma skin cancer) within 12 months prior to enrollment, chronic kidney disease with estimated glomerular filtration rate (eGFR) less than 30 or on dialysis prior to acute pancreatitis, decompensated cirrhosis, or any other medical condition with life expectancy less than 12 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented history of transplant, AIDS, cancer treatment, kidney disease, or cirrhosis status"
          },
          {
            "text": "Known pregnancy at the time of enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient is male; pregnancy status not applicable but not explicitly addressed"
          },
          {
            "text": "Incarceration",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided regarding incarceration status"
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Acute pancreatitis meets inclusion intent; eligibility hinges on absence of chronic pancreatitis on imaging and ability to complete longitudinal follow-up—both unresolved."
      },
      {
        "nct_id": "NCT07144917",
        "title": "Immunoparalysis After Pancreaticoduodenectomy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Any patient undergoing a Pancreaticoduodenectomy in one of the four participating centers for a benign or malignant tumor of the pancreatic head",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of pancreaticoduodenectomy procedure or pancreatic head tumor diagnosis in vignette."
          },
          {
            "text": "Age < 18 years",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Age: 54 years old",
            "reasoning": "Patient is 54 years old, not under 18 years."
          },
          {
            "text": "Pregnant, postpartum, or breastfeeding women",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Sex: Male",
            "reasoning": "Patient is male; criterion applies only to women."
          },
          {
            "text": "Indication other than tumor-related (e.g., chronic pancreatitis)",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Chronic alcohol use presents with severe epigastric pain radiating to the back, nausea, and vomiting. Labs reveal markedly elevated serum lipase and amylase.",
            "reasoning": "Clinical presentation consistent with acute pancreatitis, likely chronic pancreatitis indication, not tumor-related."
          },
          {
            "text": "Patient with an infectious syndrome at the time of inclusion",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about active infectious syndrome at time of inclusion."
          },
          {
            "text": "Preoperative immunosuppression",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of preoperative immunosuppression in patient history."
          },
          {
            "text": "Congenital or acquired immune deficiency",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about congenital or acquired immune deficiency."
          },
          {
            "text": "Functional hyposplenism or asplenia, patient under long-term antibiotic prophylaxis for this reason",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of functional hyposplenism, asplenia, or antibiotic prophylaxis."
          },
          {
            "text": "Patient with HIV (and CD4 < cells/mm³)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No HIV status documented in vignette."
          },
          {
            "text": "Aplasia defined by circulating neutrophil count < 500 cells/mm³",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No neutrophil count provided in patient data."
          },
          {
            "text": "Immunosuppressive treatment other than chemotherapy: Biotherapy, Corticosteroid therapy >10 mg/day or cumulative dose >700 mg prednisolone equivalent, or patient expected to receive immunosuppressive treatment within the first 7 postoperative days",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about immunosuppressive treatments, biotherapy, or corticosteroids."
          },
          {
            "text": "Individuals deprived of liberty by judicial or administrative decision",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of judicial or administrative liberty deprivation."
          },
          {
            "text": "Adults under legal protection (guardianship or curatorship)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about legal protection status or guardianship."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: indication is acute pancreatitis from alcohol use, not tumor-related pancreaticoduodenectomy candidate."
      },
      {
        "nct_id": "NCT06113419",
        "title": "Timing of CHolecystectomy In Severe PAncreatitis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥18 years",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "54-year-old man",
            "reasoning": "Patient is 54 years old, which meets age ≥18 years requirement."
          },
          {
            "text": "Diagnosis of pancreatitis according to Atlanta guidelines",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Severe epigastric pain radiating to the back, nausea, vomiting, markedly elevated serum lipase and amylase",
            "reasoning": "Clinical presentation and labs consistent with pancreatitis, but Atlanta guidelines require imaging and additional criteria not fully documented."
          },
          {
            "text": "Moderately severe or severe pancreatitis (APACHE score ≥8 on admittance)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "APACHE score on admission not provided in vignette; cannot assess severity threshold."
          },
          {
            "text": "Biliary pancreatitis diagnosed on imaging (ultrasound, magnetic resonance imaging and/or tomography)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No imaging results (ultrasound, MRI, CT) provided to confirm biliary etiology or exclude other causes."
          },
          {
            "text": "Recovery of pancreatitis by tolerance of oral intake defined as 24 hours of food consumption of any consistency without emetic episodes and pain ≤4/10 on the visual analogue score of pain",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient currently in acute phase with vomiting; no information on recovery status or pain resolution."
          },
          {
            "text": "Written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Consent status not addressed in clinical vignette."
          },
          {
            "text": "Pregnancy",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Male",
            "reasoning": "Patient is male; criterion excludes pregnancy, which is not applicable."
          },
          {
            "text": "History of cholecystectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of cholecystectomy mentioned or explicitly denied."
          },
          {
            "text": "Planned open cholecystectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No surgical planning information provided in vignette."
          },
          {
            "text": "Pancreatitis-associated complication before laparoscopic cholecystectomy (compartment syndrome, bleeding and/or need for peripancreatic collection drainage)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of complications such as compartment syndrome, bleeding, or drainage procedures."
          },
          {
            "text": "Chronic pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "History indicates chronic alcohol use but does not explicitly state chronic pancreatitis diagnosis."
          },
          {
            "text": "More than one episode of pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Number of prior pancreatitis episodes not documented in vignette."
          },
          {
            "text": "Active malignant disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No malignant disease history mentioned or excluded in vignette."
          },
          {
            "text": "Septic shock",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Septic shock status not addressed; patient is acutely ill but no sepsis documentation."
          },
          {
            "text": "Choledocholithiasis not resolved by ERCP, post-ERCP perforation and post-ERCP concomitant pancreatitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information on choledocholithiasis, ERCP, or post-ERCP complications provided."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: patient is male, triggering pregnancy exclusion criterion (likely administrative error); pancreatitis severity and biliary etiology unconfirmed."
      }
    ],
    "questions": [
      {
        "field": "Current medications and contraindicated conditions",
        "question": "What medications is the patient currently taking, and does he have any history of liver disease, kidney disease, or other significant medical conditions?",
        "why": "Affects 6 trial criteria; identifies contraindicated drugs and major comorbidities."
      },
      {
        "field": "Imaging findings (CT/MRI/MRCP)",
        "question": "Has imaging been performed to confirm pancreatitis and assess for complications like necrosis, fluid collections, or ductal obstruction?",
        "why": "Affects 3 criteria; determines pancreatitis type/severity and trial eligibility."
      },
      {
        "field": "Pancreatitis history and complications",
        "question": "Is this his first episode of pancreatitis, or does he have a history of recurrent or chronic pancreatitis?",
        "why": "Affects 4 criteria; distinguishes acute from chronic and identifies exclusionary complications."
      }
    ],
    "reeval": {
      "extended_record": "Patient presents with acute pancreatitis confirmed on CT abdomen/pelvis showing pancreatic edema and peripancreatic inflammation without necrosis or fluid collections; main pancreatic duct is patent. This is his third documented episode of acute pancreatitis in 18 months, with prior episodes in June 2022 and March 2023, all attributed to alcohol use. Current medications include omeprazole 20 mg daily for GERD and lisinopril 10 mg daily for hypertension. Past medical history includes hypertension, GERD, and mild hepatic steatosis noted on ultrasound 2 years ago. Liver function tests today show AST 78 U/L, ALT 62 U/L, alkaline phosphatase 95 U/L, total bilirubin 1.2 mg/dL; INR 1.1. Serum creatinine 0.9 mg/dL and BUN 16 mg/dL, indicating preserved renal function. Current lipase 1,240 U/L and amylase 890 U/L. Patient denies active hepatitis symptoms and reports no prior kidney disease.",
      "answers": [
        {
          "question": "What medications is the patient currently taking, and does he have any history of liver disease, kidney disease, or other significant medical conditions?",
          "answer": "Currently taking omeprazole 20 mg daily and lisinopril 10 mg daily. Has history of GERD, hypertension, and mild hepatic steatosis. No kidney disease; liver function tests show mild elevation of transaminases but preserved synthetic function.",
          "evidence_quote": "Current medications include omeprazole 20 mg daily for GERD and lisinopril 10 mg daily for hypertension. Past medical history includes hypertension, GERD, and mild hepatic steatosis noted on ultrasound 2 years ago. Liver function tests today show AST 78 U/L, ALT 62 U/L, alkaline phosphatase 95 U/L, total bilirubin 1.2 mg/dL; INR 1.1. Serum creatinine 0.9 mg/dL and BUN 16 mg/dL, indicating preserved renal function."
        },
        {
          "question": "Has imaging been performed to confirm pancreatitis and assess for complications like necrosis, fluid collections, or ductal obstruction?",
          "answer": "CT abdomen/pelvis confirms acute pancreatitis with pancreatic edema and peripancreatic inflammation. No evidence of necrosis, fluid collections, or ductal obstruction; main pancreatic duct is patent.",
          "evidence_quote": "CT abdomen/pelvis showing pancreatic edema and peripancreatic inflammation without necrosis or fluid collections; main pancreatic duct is patent."
        },
        {
          "question": "Is this his first episode of pancreatitis, or does he have a history of recurrent or chronic pancreatitis?",
          "answer": "This is his third documented episode of acute pancreatitis. Prior episodes occurred in June 2022 and March 2023, all attributed to alcohol use.",
          "evidence_quote": "This is his third documented episode of acute pancreatitis in 18 months, with prior episodes in June 2022 and March 2023, all attributed to alcohol use."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06401577",
          "criterion": "Diagnosis of definite chronic pancreatitis (CP) at enrollment based on parenchymal or ductal calcifications on CT scan, or intraductal filling defects suggestive of calcifications on MRI and/or MRCP",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Confirmed or suspected cystic tumor associated with main pancreatic duct dilation, or believed to be the cause of acute pancreatitis",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06401577",
          "criterion": "Use of disallowed concomitant medications within 30 days prior to enrollment",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        },
        {
          "nct_id": "NCT07144917",
          "criterion": "Patient with an infectious syndrome at the time of inclusion",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07144917",
          "criterion": "Functional hyposplenism or asplenia, patient under long-term antibiotic prophylaxis for this reason",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Biliary pancreatitis diagnosed on imaging (ultrasound, magnetic resonance imaging and/or tomography)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Pancreatitis-associated complication before laparoscopic cholecystectomy (compartment syndrome, bleeding and/or need for peripancreatic collection drainage)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Chronic pancreatitis",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "More than one episode of pancreatitis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Active malignant disease",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Septic shock",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06113419",
          "criterion": "Choledocholithiasis not resolved by ERCP, post-ERCP perforation and post-ERCP concomitant pancreatitis",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06179459",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Acute pancreatitis suspected, but unclear if pancreatic fluid collections present or whether endoscopic management will be performed."
        },
        {
          "nct_id": "NCT06401577",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Acute pancreatitis confirmed by elevated lipase/amylase; unclear if post-ERCP etiology, hospitalization duration, or prior necrosectomy history."
        },
        {
          "nct_id": "NCT06113419",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: no imaging evidence of biliary etiology demonstrated; history of chronic alcohol use suggests prior pancreatitis episodes."
        },
        {
          "nct_id": "NCT07144917",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: acute pancreatitis from chronic alcohol use is non-tumor indication; trial requires tumor-related pancreaticoduodenectomy only."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S002",
    "patient_text": "A 29-year-old woman presents with intermittent palpitations, heat intolerance, and unintentional weight loss. Physical exam reveals a fine tremor, tachycardia, and a diffusely enlarged, non-tender thyroid gland.",
    "extraction": [
      {
        "name": "Age",
        "value": "29 years old",
        "evidence_quote": "A 29-year-old woman"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "29-year-old woman"
      },
      {
        "name": "Palpitations",
        "value": "Present, intermittent",
        "evidence_quote": "intermittent palpitations"
      },
      {
        "name": "Heat Intolerance",
        "value": "Present",
        "evidence_quote": "heat intolerance"
      },
      {
        "name": "Unintentional Weight Loss",
        "value": "Present",
        "evidence_quote": "unintentional weight loss"
      },
      {
        "name": "Tremor",
        "value": "Fine tremor noted on exam",
        "evidence_quote": "a fine tremor"
      },
      {
        "name": "Heart Rate",
        "value": "Tachycardia",
        "evidence_quote": "tachycardia"
      },
      {
        "name": "Thyroid Gland",
        "value": "Diffusely enlarged, non-tender",
        "evidence_quote": "a diffusely enlarged, non-tender thyroid gland"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06963203",
        "title": "Thyroidectomy for Graves' Disease or Amiodarone-induced Thyrotoxicosis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Adult patients (≥ 18 years of age)",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "29-year-old woman",
            "reasoning": "Patient is 29 years old, clearly ≥18 years of age."
          },
          {
            "text": "Undergoing surgical treatment for Graves' disease or Amiodarone-induced thyrotoxicosis (AIT)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette describes clinical presentation consistent with Graves' disease but does not confirm diagnosis or mention surgical treatment."
          },
          {
            "text": "Biochemically confirmed hyperthyroidism or on specific medication for the treatment of Graves' disease or AIT",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Clinical signs suggest hyperthyroidism but no biochemical labs or medication information provided to confirm."
          },
          {
            "text": "Patients providing signed informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided regarding informed consent status."
          },
          {
            "text": "Children and minors (< 18 years)",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "29-year-old woman",
            "reasoning": "Patient is 29 years old; exclusion for <18 years does not apply."
          },
          {
            "text": "Pregnant women",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided regarding pregnancy status."
          },
          {
            "text": "Patients unable or unwilling to provide informed consent due to language barriers or intellectual limitations",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about language barriers or intellectual limitations."
          },
          {
            "text": "Patients undergoing concurrent parathyroidectomy for primary or secondary hyperparathyroidism",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of parathyroidectomy or hyperparathyroidism."
          },
          {
            "text": "Patients undergoing concurrent lymph node clearance",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of concurrent lymph node clearance procedure."
          },
          {
            "text": "Patients undergoing redo surgery",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about prior thyroid surgery or redo status."
          },
          {
            "text": "Surgical procedures performed for other reasons than Graves' disease or AIT",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Clinical presentation suggests thyroid disease but surgical indication not explicitly stated."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Clinical presentation consistent with Graves' disease (goiter, tremor, tachycardia, weight loss); eligibility uncertain pending biochemical confirmation and surgical candidacy determination."
      },
      {
        "nct_id": "NCT05461820",
        "title": "Effects of Different Treatment Schemes on the Regulation and Recurrence of Graves' Disease",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Graves hyperthyroidism (responsible for doctors' clinical diagnosis)",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Diffusely enlarged thyroid, palpitations, heat intolerance, weight loss, tremor, tachycardia consistent with hyperthyroidism, but clinical diagnosis attribution to Graves disease specifically not confirmed in vignette",
            "reasoning": "Clinical presentation consistent with Graves but no explicit diagnosis stated; requires TRAb confirmation."
          },
          {
            "text": "Age 18-65, for both men and women",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 29 years old",
            "reasoning": "Patient age 29 falls within 18-65 year inclusion range."
          },
          {
            "text": "Thyroid receptor antibody (TRAb) was positive",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "TRAb status not mentioned in vignette or extracted fields."
          },
          {
            "text": "Take part in this research voluntarily and sign the informed consent form",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Voluntariness and informed consent status not addressed in clinical vignette."
          },
          {
            "text": "Those who have used glucocorticoid or other immunosuppressants for a long time within 3 months before being selected",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about glucocorticoid or immunosuppressant use history."
          },
          {
            "text": "Those who have participated in any other drug trials within 3 months before being selected",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about prior participation in other drug trials."
          },
          {
            "text": "Patients with a history of malignant tumors",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No malignancy history mentioned in vignette."
          },
          {
            "text": "Ill-controlled hypertension: diastolic blood pressure≥100mmHg, systolic blood pressure ≥160 mmHg",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Blood pressure values not provided in vignette."
          },
          {
            "text": "Blood routine: the total number of white blood cells < 3.0×109 or neutrophils < 1.5× 109",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Complete blood count and differential not reported in vignette."
          },
          {
            "text": "Other thyroid diseases: such as subacute thyroiditis, thyroid nodules, high-function adenoma",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Diffusely enlarged thyroid gland noted; no mention of nodules, subacute thyroiditis, or adenoma",
            "reasoning": "Diffuse enlargement fits Graves but nodules/adenoma not explicitly excluded."
          },
          {
            "text": "Alanine aminotransferase(ALT) or aspartate amino transferase(AST) is greater than 2 times of the normal upper limit; or when ALT or AST is less than 2 times of the normal upper limit and the test of hepatitis B two half-and-half positive",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Liver function tests and hepatitis B serology not provided."
          },
          {
            "text": "Renal insufficiency: serum creatinine is higher than the upper limit of normal value",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Serum creatinine and renal function not mentioned."
          },
          {
            "text": "Patients with heart failure",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Tachycardia present; no clinical signs of heart failure documented, but cardiac assessment incomplete",
            "reasoning": "Tachycardia present but no mention of congestion, edema, or formal heart failure diagnosis."
          },
          {
            "text": "Patients with coronary heart disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about coronary artery disease history."
          },
          {
            "text": "Patients with other autoimmune diseases",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No other autoimmune diseases mentioned; cannot exclude possibility."
          },
          {
            "text": "Patients who are known to be allergic to any component of this medicine, allergic to the active ingredients or any auxiliary materials in the prescription",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No allergy history documented in vignette."
          },
          {
            "text": "Pregnant and lactating women or women who cannot rule out the possibility of pregnancy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Pregnancy/lactation status not addressed in clinical vignette."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Clinical diagnosis of Graves' disease likely based on presentation; eligibility uncertain pending TRAb positivity confirmation and consent."
      },
      {
        "nct_id": "NCT06392906",
        "title": "Orbital Radiotherapy in Grave's Ophthalmopathy 1 Week vs 2 Weeks (OraGO-1 Trial)",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Patient with active moderate to severe thyroid eye disease with a CAS > 4 with or without diplopia before starting IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of thyroid eye disease, CAS score, or diplopia in vignette."
          },
          {
            "text": "Patient with poor response to 3 doses of IVMP (CAS drop < 1) or CAS score > 3 after 3 doses of IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about IVMP treatment or CAS scoring provided."
          },
          {
            "text": "Patients with diplopia after 3 doses of IVMP",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of diplopia or IVMP treatment response."
          },
          {
            "text": "Patients with Graves' Ophthalmopathy who have maintained euthyroidism",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of Graves' Ophthalmopathy or thyroid function status."
          },
          {
            "text": "Non-pregnant adults aged 35 years or older",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 29 years old",
            "reasoning": "Patient is 29 years old; criterion requires 35 years or older."
          },
          {
            "text": "Individuals with severe hypertension",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No blood pressure measurements or hypertension diagnosis documented."
          },
          {
            "text": "Individuals with diabetic retinopathy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No ophthalmologic examination or diabetic retinopathy screening mentioned."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Ineligible: patient is 29 years old; trial requires age ≥35 years. No thyroid eye disease mentioned in vignette."
      },
      {
        "nct_id": "NCT05678374",
        "title": "Exploring Immunological Markers Associated With Mental Fatigue in Graves' Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "Graves' disease with positive TSH-receptor antibodies and thyroid hormones above the upper reference limit at diagnosis",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "TSH-receptor antibodies, thyroid hormone levels at diagnosis not provided in vignette."
          },
          {
            "text": "Diagnosis 15 to 60 months ago, or if recidive both episodes must have occurred within 15 months to 60 months",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about diagnosis timing or recidive episodes provided."
          },
          {
            "text": "Thyroid hormones within normal range without anti thyroid drugs",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Current thyroid hormone levels and anti-thyroid drug use not documented."
          },
          {
            "text": "No thyroid disease if control participant",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "diffusely enlarged, non-tender thyroid gland",
            "reasoning": "Patient has thyroid disease (enlarged gland with clinical hyperthyroidism), disqualifying for control."
          },
          {
            "text": "Mental Fatigue Score ≤8 if patient and control without mental fatigue",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Mental Fatigue Score not assessed in vignette."
          },
          {
            "text": "Mental Fatigue Score >13 and debut of symptoms of mental fatigue in parallel with debut of Graves' disease, without other obvious cause if patient with mental fatigue",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Mental Fatigue Score and temporal relationship with disease onset not documented."
          },
          {
            "text": "Person unable to follow protocol",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about protocol adherence ability provided."
          },
          {
            "text": "Multiple sclerosis, myalgic encephalomyelitis/chronic fatigue syndrome, or any other neurological disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of MS, ME/CFS, or other neurological disease documented."
          },
          {
            "text": "Traumatic brain injury with unconsciousness",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of traumatic brain injury mentioned."
          },
          {
            "text": "Other disease strongly associated with fatigue",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No other chronic fatigue-associated diseases documented in vignette."
          },
          {
            "text": "Pregnancy and breast-feeding",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Pregnancy and breast-feeding status not documented."
          },
          {
            "text": "On-going or recent systemic treatment with steroids",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Systemic steroid use not mentioned in vignette."
          },
          {
            "text": "Radioiodine therapy within the last 18 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Radioiodine therapy history not documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Ineligible: patient is newly presenting with Graves' disease; trial requires diagnosis 15-60 months prior. Biochemical confirmation and TSH-receptor antibody status unknown."
      }
    ],
    "questions": [
      {
        "field": "Thyroid-specific serology and hormone levels",
        "question": "What are the patient's current TSH, free T4, free T3, and TPO/TSI antibody levels?",
        "why": "Confirms Graves' disease and current thyroid status; affects 4 trial criteria"
      },
      {
        "field": "Cardiac assessment and blood pressure",
        "question": "What is the patient's current heart rate, blood pressure, and has cardiac evaluation (EKG or echocardiogram) been performed?",
        "why": "Identifies cardiac contraindications and arrhythmias from thyrotoxicosis; affects 4 criteria"
      },
      {
        "field": "Prior treatments and comorbid neurological/autoimmune conditions",
        "question": "What prior thyroid treatments (antithyroids, radioiodine, surgery) has the patient received, and does she have any other autoimmune or neurological conditions?",
        "why": "Excludes contraindicated therapies and confounding systemic diseases; affects 6 criteria"
      }
    ],
    "reeval": {
      "extended_record": "Patient presents at 8 weeks post-initial diagnosis. Current laboratory studies show TSH <0.01 mIU/L (ref 0.4–4.0), free T4 4.2 ng/dL (ref 0.8–1.8), and free T3 8.5 pg/mL (ref 2.3–4.2), consistent with active hyperthyroidism. TSI (thyroid-stimulating immunoglobulin) is markedly elevated at 8.2 IU/L (ref <1.75), confirming Graves disease; TPO antibodies negative. Vital signs today: heart rate 118 bpm (regular), blood pressure 128/76 mmHg. Twelve-lead EKG performed last week showed sinus tachycardia without ischemic changes; transthoracic echocardiogram demonstrates normal left ventricular ejection fraction (58%), mild left atrial enlargement, and no valvular pathology. Patient initiated on propranolol 40 mg twice daily 6 weeks ago for symptom control and methimazole 10 mg three times daily 5 weeks ago; no prior radioiodine or thyroidectomy. No history of other autoimmune conditions (negative tissue transglutaminase, normal CBC). Neurological exam normal; no tremor documented today after propranolol initiation.",
      "answers": [
        {
          "question": "What are the patient's current TSH, free T4, free T3, and TPO/TSI antibody levels?",
          "answer": "TSH <0.01 mIU/L, free T4 4.2 ng/dL, free T3 8.5 pg/mL, TSI 8.2 IU/L (elevated), TPO antibodies negative.",
          "evidence_quote": "Current laboratory studies show TSH <0.01 mIU/L (ref 0.4–4.0), free T4 4.2 ng/dL (ref 0.8–1.8), and free T3 8.5 pg/mL (ref 2.3–4.2), consistent with active hyperthyroidism. TSI (thyroid-stimulating immunoglobulin) is markedly elevated at 8.2 IU/L (ref <1.75), confirming Graves disease; TPO antibodies negative."
        },
        {
          "question": "What is the patient's current heart rate, blood pressure, and has cardiac evaluation (EKG or echocardiogram) been performed?",
          "answer": "Heart rate 118 bpm (regular), blood pressure 128/76 mmHg. EKG shows sinus tachycardia without ischemic changes; echocardiogram demonstrates normal LVEF (58%), mild left atrial enlargement, and no valvular pathology.",
          "evidence_quote": "Vital signs today: heart rate 118 bpm (regular), blood pressure 128/76 mmHg. Twelve-lead EKG performed last week showed sinus tachycardia without ischemic changes; transthoracic echocardiogram demonstrates normal left ventricular ejection fraction (58%), mild left atrial enlargement, and no valvular pathology."
        },
        {
          "question": "What prior thyroid treatments (antithyroids, radioiodine, surgery) has the patient received, and does she have any other autoimmune or neurological conditions?",
          "answer": "Patient initiated on methimazole 10 mg three times daily and propranolol 40 mg twice daily approximately 5–6 weeks ago; no prior radioiodine or thyroidectomy. No other autoimmune conditions identified; neurological exam normal.",
          "evidence_quote": "Patient initiated on propranolol 40 mg twice daily 6 weeks ago for symptom control and methimazole 10 mg three times daily 5 weeks ago; no prior radioiodine or thyroidectomy. No history of other autoimmune conditions (negative tissue transglutaminase, normal CBC). Neurological exam normal; no tremor documented today after propranolol initiation."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06963203",
          "criterion": "Biochemically confirmed hyperthyroidism or on specific medication for the treatment of Graves' disease or AIT",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Thyroid receptor antibody (TRAb) was positive",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Those who have used glucocorticoid or other immunosuppressants for a long time within 3 months before being selected",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Ill-controlled hypertension: diastolic blood pressure≥100mmHg, systolic blood pressure ≥160 mmHg",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Patients with heart failure",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Patients with coronary heart disease",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05461820",
          "criterion": "Patients with other autoimmune diseases",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06392906",
          "criterion": "Individuals with severe hypertension",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Graves' disease with positive TSH-receptor antibodies and thyroid hormones above the upper reference limit at diagnosis",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Thyroid hormones within normal range without anti thyroid drugs",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Multiple sclerosis, myalgic encephalomyelitis/chronic fatigue syndrome, or any other neurological disease",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "On-going or recent systemic treatment with steroids",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05678374",
          "criterion": "Radioiodine therapy within the last 18 months",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06963203",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Clinical presentation consistent with Graves' disease; eligibility depends on whether patient undergoes thyroidectomy and consents to participation."
        },
        {
          "nct_id": "NCT05461820",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Clinical diagnosis of Graves' hyperthyroidism appears likely based on presentation; eligibility contingent on informed consent and no recent trial participation."
        },
        {
          "nct_id": "NCT06392906",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient is 29 years old; trial requires age ≥35 years. No evidence of thyroid eye disease documented."
        },
        {
          "nct_id": "NCT05678374",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires euthyroid state without antithyroid drugs; patient has active hyperthyroidism requiring treatment."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S003",
    "patient_text": "A 7-year-old boy with a 3-week history of periorbital edema and frothy urine. Urinalysis shows heavy proteinuria without hematuria, and serum albumin is low.",
    "extraction": [
      {
        "name": "Age",
        "value": "7 years old",
        "evidence_quote": "A 7-year-old boy"
      },
      {
        "name": "Sex",
        "value": "male",
        "evidence_quote": "7-year-old boy"
      },
      {
        "name": "Symptom: Periorbital edema",
        "value": "present",
        "evidence_quote": "3-week history of periorbital edema"
      },
      {
        "name": "Symptom: Frothy urine",
        "value": "present",
        "evidence_quote": "frothy urine"
      },
      {
        "name": "Duration of symptoms",
        "value": "3 weeks",
        "evidence_quote": "3-week history of periorbital edema and frothy urine"
      },
      {
        "name": "Urinalysis: Proteinuria",
        "value": "heavy",
        "evidence_quote": "Urinalysis shows heavy proteinuria"
      },
      {
        "name": "Urinalysis: Hematuria",
        "value": "absent",
        "evidence_quote": "heavy proteinuria without hematuria"
      },
      {
        "name": "Serum albumin",
        "value": "low",
        "evidence_quote": "serum albumin is low"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT04571658",
        "title": "NEPTUNE Match Study",
        "phase": "NA",
        "criteria": [
          {
            "text": "Consented and eligible participants in the biopsied or non-biopsied cohorts of the NEPTUNE observational study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about NEPTUNE study enrollment or consent status."
          },
          {
            "text": "Must be potentially eligible for the NEPTUNE Match partnering trials",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about eligibility for NEPTUNE Match partnering trials available."
          },
          {
            "text": "Regular nephrology healthcare provided at a NEPTUNE study site",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about whether nephrology care is provided at a NEPTUNE site."
          },
          {
            "text": "Willing and able to consent, and as appropriate assent, to participate in NEPTUNE Match",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient/guardian willingness or ability to consent/assent provided."
          },
          {
            "text": "Currently non-NEPTUNE observational study participants are not eligible to be matched to a clinical trial using these biomarker assessments",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about current NEPTUNE observational study participation status."
          },
          {
            "text": "Non-English or non-Spanish speaking",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient or guardian language spoken provided."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Patient may have nephrotic syndrome requiring kidney biopsy and nephrology care at NEPTUNE site; prior NEPTUNE enrollment status unknown."
      },
      {
        "nct_id": "NCT06162546",
        "title": "ARREST-NEPHROSIS - Austrian Resistant Nephrotic Syndrome Treatment Response Registry and Biobank",
        "phase": "NA",
        "criteria": [
          {
            "text": "Resistant to standard immunosuppressive agents (if clinically indicated, e.g. primary/non-genetic forms)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about previous immunosuppressive treatment or response provided."
          },
          {
            "text": "Persistent urinary protein-to-creatinine (UP/C) ratio >1.0 g/g",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Heavy proteinuria without hematuria",
            "reasoning": "Heavy proteinuria present, but UP/C ratio not numerically quantified; cannot confirm >1.0 g/g threshold."
          },
          {
            "text": "eGFR > 30 ml/min per 1.73 m2",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No eGFR or serum creatinine value provided in vignette."
          },
          {
            "text": "Biopsy or a disease-causing genetic mutation associated with nephrotic syndrome",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No biopsy findings or genetic mutation testing results documented."
          },
          {
            "text": "Inability or unwillingness to comply with repeated assessments",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient or family willingness to comply with assessments."
          },
          {
            "text": "Objections against participation at discretion of the investigator",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Investigator discretion criterion; cannot be determined from clinical data alone."
          },
          {
            "text": "Secondary nephrotic syndrome",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Periorbital edema, frothy urine, heavy proteinuria, low serum albumin",
            "reasoning": "Clinical presentation consistent with nephrotic syndrome, but no secondary causes (infection, malignancy, drugs) documented or ruled out."
          },
          {
            "text": "Steroid-dependence or frequently relapsing disease (except achievement of complete remission)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior steroid treatment history, relapse pattern, or remission status documented."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Presents with nephrotic syndrome; steroid-resistance status, exact proteinuria level, and renal function need confirmation to assess eligibility."
      },
      {
        "nct_id": "NCT06607991",
        "title": "Blinatumomab for CNI-Resistant/Intolerant SRNS in Children",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Age between 2 and 17 years, regardless of gender",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 7 years old",
            "reasoning": "Patient is 7 years old, which falls within the 2-17 year age range."
          },
          {
            "text": "Meet the 2021 KDIGO definition of steroid-resistant nephrotic syndrome (SRNS)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not provide information about prior steroid response or steroid resistance status."
          },
          {
            "text": "Have received an adequate dose of calcineurin inhibitors (CNIs) for more than 6 months without achieving at least partial remission, OR have contraindications to CNI use, OR have demonstrated inadequate response or disease relapse after treatment with at least two immunosuppressive agents",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about prior CNI therapy, duration, response, or other immunosuppressive treatments."
          },
          {
            "text": "Renal biopsy performed prior to screening confirms a diagnosis of minimal change disease (MCD) or focal segmental glomerulosclerosis (FSGS)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not mention renal biopsy results or pathologic diagnosis."
          },
          {
            "text": "The subject and/or their legal guardian must provide written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about informed consent status; investigator discretion required."
          },
          {
            "text": "eGFR < 60 mL/min/1.73 m² (using the modified Bedside Schwartz formula)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No eGFR or serum creatinine values provided to calculate kidney function."
          },
          {
            "text": "Stroke or seizure within 6 months prior to screening, or other active central nervous system disorders",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about stroke, seizure, or CNS disorders in past 6 months."
          },
          {
            "text": "Genetic nephropathy confirmed by genetic testing",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No genetic testing results mentioned in vignette."
          },
          {
            "text": "Renal biopsy confirming IgA nephropathy, membranous nephropathy, or membranoproliferative glomerulonephritis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Renal biopsy pathology not specified; cannot exclude IgA, membranous, or MPGN."
          },
          {
            "text": "Positive for hepatitis B surface antigen (HBsAg), hepatitis B core antibody (HBcAb) with HBV DNA levels above normal range, hepatitis C virus (HCV) antibodies with HCV RNA levels above normal range, human immunodeficiency virus (HIV) antibodies, syphilis, or cytomegalovirus (CMV) DNA",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No infectious serology or viral/bacterial screening results provided."
          },
          {
            "text": "Moderate to severe neutropenia (≤1.0×10⁹/L), moderate to severe anemia (hemoglobin ≤90 g/L), thrombocytopenia (≤75×10⁹/L), or liver dysfunction (ALT, AST, or bilirubin greater than 2.5 times the upper limit of normal persisting for 2 weeks)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No CBC, liver function tests, or hemoglobin values documented."
          },
          {
            "text": "Received rituximab or cyclophosphamide therapy within the past 3 months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior rituximab or cyclophosphamide therapy history mentioned."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 3,
        "rationale": "Clinical picture consistent with steroid-resistant nephrotic syndrome in children; requires biopsy confirmation of MCD/FSGS and CNI-resistance documentation."
      },
      {
        "nct_id": "NCT06334692",
        "title": "Autoantibodies Against-nephrin in Idiopathic Nephrotic Syndrome",
        "phase": "NA",
        "criteria": [
          {
            "text": "Adult (>18 years) males and females",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 7 years old",
            "reasoning": "Patient is 7 years old; criterion requires age >18 years."
          },
          {
            "text": "Patients with biopsy-proven idiopathic MCD or FSGS (cases)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No kidney biopsy results provided; cannot confirm MCD or FSGS diagnosis."
          },
          {
            "text": "Patients with biopsy-proven idiopathic membranous nephropathy (controls)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No kidney biopsy results provided; cannot confirm membranous nephropathy diagnosis."
          },
          {
            "text": "Patients who provided consent to store their samples in the certified CRB biobank",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about consent or biobank storage."
          },
          {
            "text": "Reasonable possibility of a secondary cause of NS (for cases) or MN (for controls) at time of blood collections",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "7-year-old boy with periorbital edema, frothy urine, heavy proteinuria, low albumin; no hematuria",
            "reasoning": "Clinical presentation suggests MCNS, but secondary causes cannot be ruled out without full workup."
          },
          {
            "text": "Active viral or bacterial infections at time of blood collections",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not mention presence or absence of active infections at time of blood collection."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: patient is 7 years old; trial requires adults over 18 years."
      }
    ],
    "questions": [
      {
        "field": "Renal biopsy findings and diagnosis",
        "question": "Has a kidney biopsy been performed? If so, what was the histologic diagnosis (minimal change disease, FSGS, membranous nephropathy, or other)?",
        "why": "Biopsy diagnosis is critical for trial eligibility and affects 4 trial criteria."
      },
      {
        "field": "Steroid responsiveness and immunosuppressive treatment history",
        "question": "How did the patient respond to initial corticosteroid therapy, and has he received any prior immunosuppressive agents (calcineurin inhibitors, rituximab, cyclophosphamide)? If so, for how long and with what response?",
        "why": "Steroid-responsiveness and prior CNI/biologic use determine trial enrollment and affect 4 criteria."
      },
      {
        "field": "Recent infections and infectious serology",
        "question": "What are the results of recent screening for HBV, HCV, HIV, syphilis, and CMV? Are there any active infections currently?",
        "why": "Infectious status is a common exclusion criterion and affects 2 trial criteria."
      }
    ],
    "reeval": {
      "extended_record": "At 6-week follow-up, the patient presented with persistent periorbial edema and frothy urine. Kidney biopsy performed via ultrasound guidance on day 14 of illness showed diffuse foot process effacement on electron microscopy with intact glomerular basement membrane and normal immunofluorescence, consistent with minimal change disease. Serum albumin improved from 1.8 g/dL to 2.4 g/dL after 4 weeks of prednisone 2 mg/kg/day. Complete remission of proteinuria (urine protein <4 mg/kg/day) achieved by week 5 of corticosteroid therapy. No prior calcineurin inhibitors, rituximab, or cyclophosphamide required. Infectious disease screening completed: HBsAg negative, anti-HCV negative, HIV 4th generation assay negative, RPR non-reactive, and CMV IgG positive with negative CMV PCR (prior exposure, no active infection). Patient remains edema-free at current follow-up with normal renal function and urine protein excretion.",
      "answers": [
        {
          "question": "Has a kidney biopsy been performed? If so, what was the histologic diagnosis (minimal change disease, FSGS, membranous nephropathy, or other)?",
          "answer": "Yes, kidney biopsy was performed on day 14 of illness. The histologic diagnosis is minimal change disease, characterized by foot process effacement on electron microscopy with intact basement membrane and normal immunofluorescence.",
          "evidence_quote": "Kidney biopsy performed via ultrasound guidance on day 14 of illness showed diffuse foot process effacement on electron microscopy with intact glomerular basement membrane and normal immunofluorescence, consistent with minimal change disease."
        },
        {
          "question": "How did the patient respond to initial corticosteroid therapy, and has he received any prior immunosuppressive agents (calcineurin inhibitors, rituximab, cyclophosphamide)? If so, for how long and with what response?",
          "answer": "The patient achieved complete remission of proteinuria by week 5 of prednisone 2 mg/kg/day therapy with serum albumin improvement from 1.8 to 2.4 g/dL over 4 weeks. He has not received any calcineurin inhibitors, rituximab, or cyclophosphamide.",
          "evidence_quote": "Serum albumin improved from 1.8 g/dL to 2.4 g/dL after 4 weeks of prednisone 2 mg/kg/day. Complete remission of proteinuria (urine protein <4 mg/kg/day) achieved by week 5 of corticosteroid therapy. No prior calcineurin inhibitors, rituximab, or cyclophosphamide required."
        },
        {
          "question": "What are the results of recent screening for HBV, HCV, HIV, syphilis, and CMV? Are there any active infections currently?",
          "answer": "Infectious screening shows: HBsAg negative, anti-HCV negative, HIV 4th generation assay negative, RPR non-reactive, and CMV IgG positive with negative CMV PCR indicating prior exposure without active infection. No active infections present.",
          "evidence_quote": "Infectious disease screening completed: HBsAg negative, anti-HCV negative, HIV 4th generation assay negative, RPR non-reactive, and CMV IgG positive with negative CMV PCR (prior exposure, no active infection)."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06162546",
          "criterion": "Resistant to standard immunosuppressive agents (if clinically indicated, e.g. primary/non-genetic forms)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06162546",
          "criterion": "Steroid-dependence or frequently relapsing disease (except achievement of complete remission)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Meet the 2021 KDIGO definition of steroid-resistant nephrotic syndrome (SRNS)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Have received an adequate dose of calcineurin inhibitors (CNIs) for more than 6 months without achieving at least partial remission, OR have contraindications to CNI use, OR have demonstrated inadequate response or disease relapse after treatment with at least two immunosuppressive agents",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Renal biopsy performed prior to screening confirms a diagnosis of minimal change disease (MCD) or focal segmental glomerulosclerosis (FSGS)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Renal biopsy confirming IgA nephropathy, membranous nephropathy, or membranoproliferative glomerulonephritis",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06607991",
          "criterion": "Positive for hepatitis B surface antigen (HBsAg), hepatitis B core antibody (HBcAb) with HBV DNA levels above normal range, hepatitis C virus (HCV) antibodies with HCV RNA levels above normal range, human immunodeficiency virus (HIV) antibodies, syphilis, or cytomegalovirus (CMV) DNA",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06334692",
          "criterion": "Patients with biopsy-proven idiopathic MCD or FSGS (cases)",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06334692",
          "criterion": "Patients with biopsy-proven idiopathic membranous nephropathy (controls)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06334692",
          "criterion": "Active viral or bacterial infections at time of blood collections",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT04571658",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Patient with nephrotic syndrome presentation may qualify if enrolled in NEPTUNE observational cohort and eligible for partnering trials; NEPTUNE site participation status unknown."
        },
        {
          "nct_id": "NCT06334692",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient is 7 years old; trial requires adults >18 years. Also requires biopsy-proven membranous nephropathy, not yet established."
        },
        {
          "nct_id": "NCT06162546",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: no evidence of resistance to standard immunosuppressants; patient is newly presenting with nephrotic syndrome, not yet treated."
        },
        {
          "nct_id": "NCT06607991",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient does not meet steroid-resistant nephrotic syndrome criteria; no documented inadequate CNI response or multi-agent failure yet."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S004",
    "patient_text": "A 68-year-old man with a long smoking history presents with painless gross hematuria. CT urography reveals a mass in the bladder wall.",
    "extraction": [
      {
        "name": "Age",
        "value": "68 years old",
        "evidence_quote": "A 68-year-old man"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "A 68-year-old man"
      },
      {
        "name": "Smoking History",
        "value": "Long smoking history",
        "evidence_quote": "with a long smoking history"
      },
      {
        "name": "Chief Complaint",
        "value": "Painless gross hematuria",
        "evidence_quote": "presents with painless gross hematuria"
      },
      {
        "name": "Imaging Finding",
        "value": "Mass in the bladder wall",
        "evidence_quote": "CT urography reveals a mass in the bladder wall"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06709196",
        "title": "Clinical Trial Testing Whether Targeted Antibiotic Prophylaxis Can Reduce Infections After Cystectomy Compared to Empiric Prophylaxis",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Age at surgery ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 68 years old",
            "reasoning": "Patient is 68, which meets the ≥18 years requirement."
          },
          {
            "text": "Ability to understand and sign an informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's cognitive ability or capacity to consent."
          },
          {
            "text": "Malignant or benign indication for undergoing cystectomy",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Mass suggests malignancy but histologic confirmation and surgical indication not explicitly stated."
          },
          {
            "text": "Planned ileal conduit as urinary diversion",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not specify planned type of urinary diversion."
          },
          {
            "text": "Previous severe allergic reaction to antimicrobial treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of allergic reactions to antimicrobials documented."
          },
          {
            "text": "Long-term prophylactic antibiotic treatment which is expected to be continued after the cystectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about current or planned prophylactic antibiotic use."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Bladder mass likely requires cystectomy; unresolved: consent capacity, malignant indication confirmation, and ileal conduit as planned diversion."
      },
      {
        "nct_id": "NCT05944237",
        "title": "HTL0039732 in Participants With Advanced Solid Tumours",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Histologically or cytologically proven advanced solid tumour, refractory to conventional treatment, or for which no further conventional therapy is considered appropriate by the Investigator or is declined by the potential participant.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Mass identified but histologic/cytologic confirmation and treatment history not documented."
          },
          {
            "text": "At least 1 measurable lesion according to RECIST v1.1, which (in the Investigator's opinion) has had objective radiological progression on or after the last therapy, or at least one assessable lesion e.g. pleural or peritoneal thickening that does not fulfil RECIST v1.1 criteria for measurable disease.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Mass present but RECIST measurability and prior therapy response not specified in vignette."
          },
          {
            "text": "Life expectancy of at least 12 weeks.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about life expectancy estimate."
          },
          {
            "text": "Eastern Cooperative Oncology Group performance status of 0 or 1.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Performance status not documented in clinical vignette."
          },
          {
            "text": "Aged 18 years or over at the time consent is given.",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "68-year-old man",
            "reasoning": "Patient is 68 years old, exceeding the 18-year minimum requirement."
          },
          {
            "text": "Radiotherapy (except for palliative reasons), chemotherapy, non chemotherapy systemic anti-cancer therapy (apart from life-long hormone suppression such as luteinising hormone-releasing agents in participants with mCRPC) or investigational medicinal products during the 4 weeks prior to enrolment; or first dose of an immunotherapy during the previous 12 weeks before first dose of HTL0039732.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Prior treatment history and timing relative to enrolment not documented."
          },
          {
            "text": "Ongoing toxic manifestations of previous treatments that are Grade >1 per CTCAE v5.0.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior treatment toxicities documented in vignette."
          },
          {
            "text": "Any central nervous system metastases (unless potential participants have had local therapy and are asymptomatic, radiologically stable and have been off steroids for ≥4 weeks prior to enrolment).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about CNS metastases status."
          },
          {
            "text": "Known history of current or latent tuberculosis, HIV or Hepatitis B or C infection.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented history of TB, HIV, Hepatitis B or C."
          },
          {
            "text": "Prior treatment with EP4 inhibitor.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Prior EP4 inhibitor treatment not mentioned in vignette."
          },
          {
            "text": "Known active peptic ulcer disease, or symptoms of gastritis, dyspepsia or gastro-esophageal reflux disease (one or more episodes per week).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of peptic ulcer disease, gastritis, dyspepsia, or GERD symptoms."
          },
          {
            "text": "For Phase 1 Part B and Phase 2a: History or clinical suspicion of interstitial lung disease, history of (non-infectious) pneumonitis that required steroids, or current pneumonitis.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history or symptoms of interstitial lung disease or pneumonitis documented."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Bladder mass is advanced solid tumor; unresolved: histologic confirmation, RECIST-measurable progression, and 12-week life expectancy."
      },
      {
        "nct_id": "NCT04916990",
        "title": "Improving Care for Rural Patients With Solid Tumors",
        "phase": "NA",
        "criteria": [
          {
            "text": "Male and female adults over 18 years old",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "68-year-old man",
            "reasoning": "Patient is male adult over 18 years old."
          },
          {
            "text": "English or Spanish speaking",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Language ability not mentioned in vignette."
          },
          {
            "text": "Receives cancer treatment at UCH-Aurora, UCH-Highlands Ranch, UCHealth North, UCHealth South-UCHealth Memorial Hospital, UCHealth Parkview Hospital, San Juan Cancer Center, RMCC-Pueblo, SCL-St. Mary's, or Parkview Medical Center",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Treatment location not specified in vignette."
          },
          {
            "text": "Resides in any of the rural counties served by the participating centers with Rural-Urban Continuum Codes (RUCC) codes 4-9",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Residence location and RUCC code not provided."
          },
          {
            "text": "Diagnosed with lung cancer (SCLC or NSCLC) with ICD-O codes C34.0, C34.1, C34.2, C34.3, C34.8, C34.9, or C33.9, or other lung cancer variants",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Patient has bladder cancer, not lung cancer."
          },
          {
            "text": "Diagnosed with head and neck squamous cell carcinoma (HNSCC) or salivary gland cancer with specified ICD-O codes, or other head and neck cancer variants",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Patient has bladder cancer, not head and neck squamous cell carcinoma."
          },
          {
            "text": "Diagnosed with breast, cervical, colorectal, thyroid, or bladder cancer with specified ICD-O codes",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "CT urography reveals a mass in the bladder wall",
            "reasoning": "Patient has bladder cancer, which is an included cancer type."
          },
          {
            "text": "Will receive surgery, radiation therapy, chemotherapy, or a combination of those modalities (including neoadjuvant and adjuvant therapy)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Treatment plan not yet discussed in vignette."
          },
          {
            "text": "Rural and medically underserved, defined as residing in a rural county with RUCC code 4-9 AND meeting health professional shortage areas or Medically Underserved Areas/Populations criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Rural status, RUCC code, and underserved area criteria not documented."
          },
          {
            "text": "Uninsured or underinsured (no health insurance, public insurance only, or 10% or more of annual income spent on out-of-pocket medical expenses)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Insurance status and out-of-pocket expenses not mentioned."
          },
          {
            "text": "Children under 18 years old",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "68-year-old man",
            "reasoning": "Patient is 68 years old, not under 18."
          },
          {
            "text": "Diagnosed with primary cancer other than breast, bladder, cervix, colon, rectum, lung, head-and-neck cancer, or thyroid cancer",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Bladder cancer is an included primary cancer type, not excluded."
          },
          {
            "text": "Has already initiated curative treatment for the current episode of cancer",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Whether curative treatment has been initiated not documented."
          },
          {
            "text": "From vulnerable populations (inmates or on probation, homeless, or pregnant)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vulnerable population status not addressed in vignette."
          },
          {
            "text": "Decisionally-challenged with cognitive or personality impairment, suicidal ideation, or intoxication (alcohol or drugs) at the time of consent that interferes with ability to participate in the study",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Decisional capacity and mental status not evaluated in vignette."
          },
          {
            "text": "Unable to hear (not including individuals who can hear with an auditory aid)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Hearing ability not documented."
          },
          {
            "text": "Likely inability to track the individual over time (e.g., no permanent address at the time of consent)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Residence stability and contact information not provided."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: trial requires lung cancer or head/neck squamous cell carcinoma; patient has bladder cancer."
      },
      {
        "nct_id": "NCT06493370",
        "title": "Intravenous Ascorbate Plus Gemcitabine/Carboplatin: A Novel and Cost-Effective Alternative With Evident Efficacy in Patients With Muscle Invasive Bladder Cancer",
        "phase": "PHASE2",
        "criteria": [
          {
            "text": "Ability of participant to understand this study, and participant willingness to sign a written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's cognitive ability or willingness to consent."
          },
          {
            "text": "Males and females age ≥ 18 years",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "68-year-old man",
            "reasoning": "Patient is male and 68 years old, which meets age ≥18 years requirement."
          },
          {
            "text": "ECOG Performance Status (PS) 0 - 2",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "ECOG Performance Status not documented in vignette."
          },
          {
            "text": "Diagnosis/disease status Cisplatin-ineligible or declined muscle invasive bladder cancer",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Mass in the bladder wall",
            "reasoning": "Bladder mass present but cisplatin eligibility status and muscle invasiveness not explicitly confirmed."
          },
          {
            "text": "Absolute Neutrophil Count > 1.5K/UL (or between 1000-1500 for patients with established benign neutropenia at treating physician discretion)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Absolute Neutrophil Count not provided in patient fields."
          },
          {
            "text": "Platelets > 100K/UL",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Platelet count not provided in patient fields."
          },
          {
            "text": "Hemoglobin ≥ 9 g/dL",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Hemoglobin level not provided in patient fields."
          },
          {
            "text": "Serum creatinine ≤ 1.5 x upper limit of normal (ULN) or calculated creatinine clearance ≥ 30 mL/min using the Cockcroft-Gault equation",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Serum creatinine or creatinine clearance not provided."
          },
          {
            "text": "Normal Glucose-6-phosphate dehydrogenase (G6PD) status",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "G6PD status not documented in vignette."
          },
          {
            "text": "Women of childbearing potential must have a negative serum pregnancy test 72 hours prior to initiating treatment",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Male",
            "reasoning": "Patient is male; criterion applies only to women of childbearing potential."
          },
          {
            "text": "Simultaneously enrolled in any therapeutic clinical trial",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about concurrent trial enrollment."
          },
          {
            "text": "Current or anticipating use of other anti-neoplastic or investigational agents while participating in this study",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about current or anticipated use of other anti-neoplastic agents."
          },
          {
            "text": "Is pregnant or breastfeeding",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Male",
            "reasoning": "Patient is male; cannot be pregnant or breastfeeding."
          },
          {
            "text": "Has a severe known allergic reaction to any excipient contained in the study drug formulation",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented allergies to study drug excipients."
          },
          {
            "text": "Active Grade 3 or 4 viral, bacterial, or fungal infection within 2 weeks prior to the first dose of study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about active viral, bacterial, or fungal infections within 2 weeks."
          },
          {
            "text": "Uncontrolled intercurrent illness, including but not limited to, ongoing or active infection, symptomatic congestive heart failure, uncontrolled hypertension, unstable angina pectoris, cardiac arrhythmia, interstitial lung disease, serious chronic gastrointestinal conditions associated with diarrhea",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about uncontrolled intercurrent illnesses listed."
          },
          {
            "text": "Histology of pure adenocarcinoma, pure squamous cell carcinoma, or pure small cell carcinoma in the TURBT sample",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "TURBT histology not provided; only imaging finding of mass documented."
          },
          {
            "text": "Current consumption of tobacco products",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Long smoking history",
            "reasoning": "History of heavy smoking documented, but current tobacco use status unclear."
          },
          {
            "text": "History of G6PD deficiency",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented history of G6PD deficiency."
          },
          {
            "text": "History of oxalate renal calculi",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about history of oxalate renal calculi."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: trial requires negative pregnancy test; patient is male, making this criterion inapplicable."
      }
    ],
    "questions": [
      {
        "field": "Cancer treatment status and histology details",
        "question": "Has the bladder mass been biopsied/confirmed as muscle-invasive bladder cancer, and what is the histologic subtype (urothelial vs. other)?",
        "why": "Confirms diagnosis and treatment eligibility for 4 trial criteria"
      },
      {
        "field": "Complete blood count and renal function labs",
        "question": "What are the most recent CBC and comprehensive metabolic panel results, including hemoglobin, platelet count, and creatinine/eGFR?",
        "why": "Assesses safety eligibility and organ function for treatment in 4 criteria"
      },
      {
        "field": "Insurance, vulnerabilities, and ability to consent/follow-up",
        "question": "Does the patient have insurance coverage, live in a stable residence, and have reliable transportation for follow-up visits?",
        "why": "Addresses vulnerable population exclusions affecting 6 trial criteria"
      }
    ],
    "reeval": {
      "extended_record": "Patient underwent cystoscopy with transurethral resection of bladder tumor (TURBT) on 2024-01-15. Pathology confirmed high-grade urothelial carcinoma with invasion into muscularis propria, consistent with muscle-invasive bladder cancer (MIBC), stage T2. No lymphovascular invasion noted. Most recent CBC from 2024-01-22 shows hemoglobin 11.8 g/dL, platelet count 215 K/uL, WBC 7.2 K/uL. Comprehensive metabolic panel from same date: serum creatinine 1.4 mg/dL, eGFR 58 mL/min/1.73m² (Stage 3a CKD), potassium 4.1 mEq/L, albumin 3.6 g/dL. Patient has Medicare coverage with supplemental insurance. Lives with spouse in stable single-family residence; reliable transportation via personal vehicle. Employed part-time, good social support. Fit for multimodal therapy discussion.",
      "answers": [
        {
          "question": "Has the bladder mass been biopsied/confirmed as muscle-invasive bladder cancer, and what is the histologic subtype (urothelial vs. other)?",
          "answer": "Yes, confirmed muscle-invasive bladder cancer. Histologic subtype is high-grade urothelial carcinoma with invasion into muscularis propria (T2 stage).",
          "evidence_quote": "Pathology confirmed high-grade urothelial carcinoma with invasion into muscularis propria, consistent with muscle-invasive bladder cancer (MIBC), stage T2."
        },
        {
          "question": "What are the most recent CBC and comprehensive metabolic panel results, including hemoglobin, platelet count, and creatinine/eGFR?",
          "answer": "CBC (2024-01-22): hemoglobin 11.8 g/dL, platelets 215 K/uL. CMP: creatinine 1.4 mg/dL, eGFR 58 mL/min/1.73m².",
          "evidence_quote": "Most recent CBC from 2024-01-22 shows hemoglobin 11.8 g/dL, platelet count 215 K/uL, WBC 7.2 K/uL. Comprehensive metabolic panel from same date: serum creatinine 1.4 mg/dL, eGFR 58 mL/min/1.73m²"
        },
        {
          "question": "Does the patient have insurance coverage, live in a stable residence, and have reliable transportation for follow-up visits?",
          "answer": "Yes to all three. Patient has Medicare with supplemental coverage, lives in stable single-family residence with spouse, and has reliable personal vehicle transportation.",
          "evidence_quote": "Patient has Medicare coverage with supplemental insurance. Lives with spouse in stable single-family residence; reliable transportation via personal vehicle."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06493370",
          "criterion": "Platelets > 100K/UL",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06493370",
          "criterion": "Hemoglobin ≥ 9 g/dL",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT06709196",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Bladder mass likely requires cystectomy; unresolved: consent capacity, malignant indication confirmation, and ileal conduit as planned diversion."
        },
        {
          "nct_id": "NCT05944237",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Bladder mass is advanced solid tumor; unresolved: histologic confirmation, RECIST-measurable progression, and 12-week life expectancy."
        },
        {
          "nct_id": "NCT04916990",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires lung cancer or head/neck squamous cell carcinoma; patient has bladder cancer."
        },
        {
          "nct_id": "NCT06493370",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires negative pregnancy test; patient is male, making this criterion inapplicable."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S005",
    "patient_text": "A 34-year-old woman presents with recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia.",
    "extraction": [
      {
        "name": "Age",
        "value": "34 years old",
        "evidence_quote": "A 34-year-old woman"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "A 34-year-old woman"
      },
      {
        "name": "Chief Complaint",
        "value": "Recurrent episodes of severe unilateral throbbing headache",
        "evidence_quote": "recurrent episodes of severe unilateral throbbing headache"
      },
      {
        "name": "Headache Character",
        "value": "Throbbing",
        "evidence_quote": "severe unilateral throbbing headache"
      },
      {
        "name": "Headache Location",
        "value": "Unilateral",
        "evidence_quote": "severe unilateral throbbing headache"
      },
      {
        "name": "Aura",
        "value": "Visual scotomata",
        "evidence_quote": "preceded by visual scotomata"
      },
      {
        "name": "Associated Symptom - Photophobia",
        "value": "Present",
        "evidence_quote": "accompanied by photophobia"
      },
      {
        "name": "Associated Symptom - Phonophobia",
        "value": "Present",
        "evidence_quote": "accompanied by photophobia, nausea, and phonophobia"
      },
      {
        "name": "Associated Symptom - Nausea",
        "value": "Present",
        "evidence_quote": "accompanied by photophobia, nausea, and phonophobia"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06788977",
        "title": "External Trigeminal Nerve Stimulation for Migraine Treatment in Pregnancy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients willing and able to provide simple consent for registry participation",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's willingness or ability to consent."
          },
          {
            "text": "Has access to email, text messages via smartphone or computer with internet access",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about patient's access to technology."
          },
          {
            "text": "Be between the ages of 18 to 44 years at enrollment",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "A 34-year-old woman",
            "reasoning": "Patient is 34 years old, within the 18-44 age range."
          },
          {
            "text": "Pregnant with one fetus/baby at time of enrollment (singleton pregnancy)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about pregnancy status or fetal number provided."
          },
          {
            "text": "Have headaches or migraines prior to pregnancy and continued to have headaches or migraines into pregnancy OR headaches or migraines began while pregnant in the first trimester",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about pregnancy status or timing of headache onset relative to pregnancy."
          },
          {
            "text": "Able to provide proof of active intrauterine pregnancy and estimated due date via online document upload",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about pregnancy status or ability to provide documentation."
          },
          {
            "text": "Patients under the age of 18 or over the age of 44 at enrollment",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "A 34-year-old woman",
            "reasoning": "Patient is 34 years old, not under 18 or over 44."
          },
          {
            "text": "Not pregnant at time of enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about current pregnancy status provided."
          },
          {
            "text": "Pregnant with more than one fetus/baby at time of enrollment (multigestational pregnancy)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about pregnancy status or fetal number provided."
          },
          {
            "text": "Patients with any other condition which might preclude participation in the opinion of the patient's physician(s) or the study's principal investigator",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Criterion depends on physician discretion; not objectively determinable from vignette."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Migraine diagnosis confirmed; pregnancy status unknown—cannot assess eligibility without confirmation of singleton pregnancy and consent capability."
      },
      {
        "nct_id": "NCT07402954",
        "title": "Stimulation of External Carotid Artery Circulation",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age ≥18",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "A 34-year-old woman",
            "reasoning": "Patient is 34 years old, which is ≥18 years old."
          },
          {
            "text": "Chronic migraine or status migrainosus, or craniofacial pain refractory to maximal medical therapy who are undergoing MMA IA lidocaine infusion",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette describes migraine presentation but does not specify chronicity, refractoriness to treatment, or current intervention status."
          },
          {
            "text": "Subject has provided informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about informed consent status; investigator discretion."
          },
          {
            "text": "Known allergies to lidocaine",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No allergy history mentioned in vignette."
          },
          {
            "text": "Seizure disorder, history of seizures, or increased seizure susceptibility",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No seizure history or seizure disorder documented in vignette."
          },
          {
            "text": "Intracranial vascular malformations or dural AVF",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No imaging findings or vascular malformation history documented."
          },
          {
            "text": "Hemodynamic instability, any condition where brief hemodynamic shifts may pose risk",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No hemodynamic status or cardiovascular baseline documented in vignette."
          },
          {
            "text": "Previous MMA intervention or craniotomy that could result in MMA occlusion",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior MMA intervention or craniotomy history documented."
          },
          {
            "text": "Any implanted electronic device (pacemaker, ICD, DBS, VNS, cochlear implant, spinal cord stimulator)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No implanted electronic devices mentioned in vignette."
          },
          {
            "text": "Significant cardiovascular disease (unstable angina, severe arrhythmias, recent MI)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No cardiovascular disease history documented."
          },
          {
            "text": "Severe autonomic dysfunction",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No autonomic dysfunction documented in vignette."
          },
          {
            "text": "Active systemic infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No active infection documented in vignette."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Migraine confirmed; eligibility hinges on refractory status, MMA IA lidocaine infusion status, and lidocaine allergy history—all unknown."
      },
      {
        "nct_id": "NCT06785129",
        "title": "Endometriosis and Migraine",
        "phase": "NA",
        "criteria": [
          {
            "text": "Diagnosed endometriosis, migraine, or both endometriosis and migraine",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia",
            "reasoning": "Clinical presentation is classic for migraine with aura, meeting inclusion criterion."
          },
          {
            "text": "Healthy control subjects with no history of chronic pain",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata",
            "reasoning": "Patient has migraine (chronic pain condition), not a healthy control subject."
          },
          {
            "text": "Age 12-45",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "34-year-old woman",
            "reasoning": "Age 34 falls within the 12-45 year range."
          },
          {
            "text": "Assigned female sex at birth",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "34-year-old woman",
            "reasoning": "Patient is female, assigned female sex at birth."
          },
          {
            "text": "Pregnancy or breastfeeding",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not mention pregnancy or breastfeeding status."
          },
          {
            "text": "Presence of prolactinoma",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about prolactinoma presence or absence."
          },
          {
            "text": "Presence of psychiatric, neurological, endocrinological and/or developmental conditions and taking medications for these conditions",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about psychiatric, neurological, endocrinological, or developmental conditions or medications."
          },
          {
            "text": "Current use of dopamine agonist or SSRI medications",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about current dopamine agonist or SSRI medication use."
          },
          {
            "text": "For patients aged 12-17, not having a parent/legal guardian willing to sign the consent and answer surveys about their child's health",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "34-year-old woman",
            "reasoning": "Patient is 34 years old, outside the 12-17 age range requiring parental consent."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: requires healthy controls with no chronic pain history; patient has recurrent severe migraines."
      },
      {
        "nct_id": "NCT06995729",
        "title": "A Study to Learn About the Study Medicine Called Zavegepant (PF-07930207) in Children With a History of Migraine",
        "phase": "PHASE1",
        "criteria": [
          {
            "text": "Participants aged 6 years to less than 12 years",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 34 years old",
            "reasoning": "Patient is 34 years old; criterion requires age 6 to <12 years."
          },
          {
            "text": "Documented medical history of migraine with or without aura for at least 6 months before the Screening Visit",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Chief Complaint: Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia.",
            "reasoning": "Clinical presentation consistent with migraine with aura, but duration of 6+ months history not explicitly documented."
          },
          {
            "text": "Weight >15 kg at the Screening Visit",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient weight not provided in vignette or extracted fields."
          },
          {
            "text": "Evidence or history of clinically significant disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about clinically significant disease history beyond migraine."
          },
          {
            "text": "Continuous migraine (defined as an unrelenting headache) within 1 month prior to Screening Visit",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Temporal pattern of episodes not specified; cannot determine if continuous migraine occurred within 1 month."
          },
          {
            "text": "Atypical migraine types, complications of a migraine, or a confounding and clinically significant pain syndrome",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Recurrent episodes of severe unilateral throbbing headache preceded by visual scotomata, accompanied by photophobia, nausea, and phonophobia.",
            "reasoning": "Clinical presentation consistent with typical migraine with aura; no evidence of atypical types or complications."
          },
          {
            "text": "Conditions that may affect the administration or absorption of the nasal product",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about gastrointestinal or absorption conditions affecting nasal product administration."
          },
          {
            "text": "Clinically significant depression (Promis Parent Proxy SF 2.0 Depressive Scale T score ≥70)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No depression screening score (Promis Parent Proxy SF 2.0) provided."
          },
          {
            "text": "Suicidal ideation and behaviour (C-SSRS: any 'yes' to items 2 to 5 or any 'yes' to suicide behaviours)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No C-SSRS assessment or suicidal ideation/behavior information documented."
          },
          {
            "text": "Serum Total bilirubin >1.5 × ULN (Upper Limit of Normal)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Serum total bilirubin level not provided."
          },
          {
            "text": "AST (Aspartate Transferase) or ALT (Alanine Transaminase) >2 × ULN",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "AST and ALT levels not provided."
          },
          {
            "text": "Abnormal ECG (Electrocardiogram) at screening visit",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "ECG results not documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: trial enrolls children aged 6–<12 years; patient is 34 years old. Also fails atypical migraine exclusion criterion."
      }
    ],
    "questions": [
      {
        "field": "Medical history and comorbidities",
        "question": "Do you have any history of heart disease, high blood pressure, stroke, seizures, or thyroid problems?",
        "why": "Affects 7 trial criteria; most trials require absence of cardiovascular and neurological conditions."
      },
      {
        "field": "Pregnancy and reproductive status",
        "question": "Are you currently pregnant, breastfeeding, or planning pregnancy in the next year? What contraception are you using?",
        "why": "Affects 5 trial criteria; critical for safety and eligibility given potential teratogenic risk."
      },
      {
        "field": "Current medications",
        "question": "What medications are you currently taking for migraine or other conditions, including over-the-counter and supplements?",
        "why": "Affects 2 criteria; identifies contraindications and drug interactions with trial interventions."
      }
    ],
    "reeval": {
      "extended_record": "Patient reports no personal history of cardiac disease, hypertension, prior stroke, or seizure disorder. Denies current thyroid dysfunction; TSH last checked 18 months ago was 2.1 mIU/L (normal range). Not currently pregnant or breastfeeding; reports regular menses on 28-day cycle. Denies plans for pregnancy in next 12 months. Currently using copper IUD for contraception, placed 3 years ago without complications. For migraine management, patient takes sumatriptan 50 mg as needed during attacks (approximately 2–3 times monthly) with good efficacy, reducing headache duration to 4–6 hours. Also uses ibuprofen 400 mg PRN for mild headaches. Takes no daily prophylactic medications. Reports inconsistent magnesium supplementation (400 mg, 2–3 times weekly). Denies use of estrogen-containing oral contraceptives given migraine with aura. No other regular medications.",
      "answers": [
        {
          "question": "Do you have any history of heart disease, high blood pressure, stroke, seizures, or thyroid problems?",
          "answer": "No history of cardiac disease, hypertension, stroke, or seizures. No current thyroid dysfunction; TSH was normal at 2.1 mIU/L on recent screening.",
          "evidence_quote": "Patient reports no personal history of cardiac disease, hypertension, prior stroke, or seizure disorder. Denies current thyroid dysfunction; TSH last checked 18 months ago was 2.1 mIU/L (normal range)."
        },
        {
          "question": "Are you currently pregnant, breastfeeding, or planning pregnancy in the next year? What contraception are you using?",
          "answer": "Not currently pregnant or breastfeeding, with no plans for pregnancy within 12 months. Using copper IUD for contraception, placed 3 years ago.",
          "evidence_quote": "Not currently pregnant or breastfeeding; reports regular menses on 28-day cycle. Denies plans for pregnancy in next 12 months. Currently using copper IUD for contraception, placed 3 years ago without complications."
        },
        {
          "question": "What medications are you currently taking for migraine or other conditions, including over-the-counter and supplements?",
          "answer": "Takes sumatriptan 50 mg as needed during attacks (2–3 times monthly), ibuprofen 400 mg PRN, and inconsistent magnesium supplementation 400 mg. No daily prophylactic medications or estrogen-containing contraceptives.",
          "evidence_quote": "For migraine management, patient takes sumatriptan 50 mg as needed during attacks (approximately 2–3 times monthly) with good efficacy, reducing headache duration to 4–6 hours. Also uses ibuprofen 400 mg PRN for mild headaches. Takes no daily prophylactic medications. Reports inconsistent magnesium supplementation (400 mg, 2–3 times weekly). Denies use of estrogen-containing oral contraceptives given migraine with aura."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06788977",
          "criterion": "Pregnant with one fetus/baby at time of enrollment (singleton pregnancy)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06788977",
          "criterion": "Not pregnant at time of enrollment",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06788977",
          "criterion": "Pregnant with more than one fetus/baby at time of enrollment (multigestational pregnancy)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Seizure disorder, history of seizures, or increased seizure susceptibility",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07402954",
          "criterion": "Significant cardiovascular disease (unstable angina, severe arrhythmias, recent MI)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06785129",
          "criterion": "Pregnancy or breastfeeding",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06785129",
          "criterion": "Current use of dopamine agonist or SSRI medications",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06995729",
          "criterion": "Evidence or history of clinically significant disease",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT07402954",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Migraine with aura matches chronic migraine phenotype; medical optimization status and lidocaine allergy unknown; consent status unresolved."
        },
        {
          "nct_id": "NCT06785129",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires healthy controls without chronic pain history; patient has recurrent migraines."
        },
        {
          "nct_id": "NCT06788977",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires pregnancy at enrollment; patient is not pregnant."
        },
        {
          "nct_id": "NCT06995729",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient is 34 years old; trial enrolls children aged 6–11 years only."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S006",
    "patient_text": "A 45-year-old man with poorly controlled type 2 diabetes presents with fever, facial pain, black necrotic eschar on the nasal mucosa, and periorbital swelling.",
    "extraction": [
      {
        "name": "Age",
        "value": "45 years old",
        "evidence_quote": "A 45-year-old man"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "A 45-year-old man"
      },
      {
        "name": "Medical History - Diabetes",
        "value": "Poorly controlled type 2 diabetes",
        "evidence_quote": "poorly controlled type 2 diabetes"
      },
      {
        "name": "Symptom - Fever",
        "value": "Present",
        "evidence_quote": "fever"
      },
      {
        "name": "Symptom - Facial Pain",
        "value": "Present",
        "evidence_quote": "facial pain"
      },
      {
        "name": "Exam Finding - Nasal Eschar",
        "value": "Black necrotic eschar on the nasal mucosa",
        "evidence_quote": "black necrotic eschar on the nasal mucosa"
      },
      {
        "name": "Exam Finding - Periorbital Swelling",
        "value": "Present",
        "evidence_quote": "periorbital swelling"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT07339800",
        "title": "Chest CT Scan in Pulmonary Mucormycosis: Prognostic Value",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients aged 18 years or older",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "45-year-old man",
            "reasoning": "Patient is 45 years old, which meets the ≥18 years requirement."
          },
          {
            "text": "Treated at Strasbourg University Hospital between January 1, 2009, and June 3, 2025",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about where or when the patient was treated."
          },
          {
            "text": "With a diagnosis of probable or proven invasive pulmonary infection with Mucorales according to the 2020 EORTC/MSGERC criteria",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Black necrotic eschar on the nasal mucosa, fever, periorbital swelling, poorly controlled type 2 diabetes",
            "reasoning": "Clinical presentation highly suggestive of rhino-orbital mucormycosis, but no formal EORTC/MSGERC diagnostic confirmation or pulmonary involvement documented."
          },
          {
            "text": "Having undergone at least one CT scan including the thoracic region",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of whether CT scans were performed or their anatomic coverage."
          },
          {
            "text": "No CT scan including the thoracic region",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about imaging studies performed or thoracic imaging availability."
          },
          {
            "text": "No diagnosis of probable or proven invasive pulmonary infection with Mucorales according to EORTC/MSGERC 2020 criteria",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Black necrotic eschar on the nasal mucosa, fever, periorbital swelling, poorly controlled type 2 diabetes",
            "reasoning": "Clinical features suggest mucormycosis but lack formal diagnostic confirmation and unclear if pulmonary infection present."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Clinical presentation suggests rhinocerebral mucormycosis with possible pulmonary involvement, but treatment site and CT imaging confirmation status unknown."
      },
      {
        "nct_id": "NCT05406037",
        "title": "Biomarkers for Invasive Mucormycosis",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 3 to 64 years old (18 to 64 years old for controls)",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "45-year-old man",
            "reasoning": "Patient is 45 years old, within the 18-64 age range for inclusion."
          },
          {
            "text": "Informed consent obtained from participant or parent/guardian for children",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about informed consent status."
          },
          {
            "text": "Patient socially insured",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about insurance or social coverage status."
          },
          {
            "text": "For case group: diagnosis of mucormycosis confirmed by conventional mycology data and/or positivity of q-PCR and/or anatomopathologic diagnosis with compatible clinical situation",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Black necrotic eschar on the nasal mucosa, fever, facial pain, periorbital swelling, poorly controlled type 2 diabetes",
            "reasoning": "Clinical presentation highly suggestive of mucormycosis but confirmatory mycology, q-PCR, or histopathology results not provided."
          },
          {
            "text": "For control group 1: patient assessed for hematopoietic stem cell transplantation, considered at risk for IFI but with pre-transplantation review excluding ongoing infection",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "45-year-old man with poorly controlled type 2 diabetes",
            "reasoning": "Patient is not described as undergoing hematopoietic stem cell transplantation assessment; different risk profile."
          },
          {
            "text": "For control group 2: diagnosis of disseminated candidiasis or invasive pulmonary aspergillosis made according to EORTC/MSG criteria or AspICU criteria",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Black necrotic eschar on the nasal mucosa",
            "reasoning": "Clinical presentation is consistent with mucormycosis, not candidiasis or aspergillosis."
          },
          {
            "text": "Co-infection of mucormycosis with other invasive fungal infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about co-infections with other invasive fungal pathogens."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Does not meet control group criteria (no transplant or disseminated candidiasis/aspergillosis); mucormycosis diagnosis status unconfirmed by required mycology/PCR/pathology criteria."
      },
      {
        "nct_id": "NCT06440915",
        "title": "Study on Theraputic Drug Monitoring and Phamacokinetics of Isavuconazole in Children",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients who intend to take isavuconazole for the treatment of invasive mycosis",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Black necrotic eschar on the nasal mucosa, fever, periorbital swelling in poorly controlled diabetic patient",
            "reasoning": "Clinical presentation suggests rhinocerebral mucormycosis (invasive mycosis), but diagnosis not confirmed in vignette."
          },
          {
            "text": "Aged 0-18 years",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "45-year-old man",
            "reasoning": "Patient is 45 years old, not in the 0-18 year age range specified."
          },
          {
            "text": "The subject and his/her guardian are willing to comply with the procedures and operations specified in the study protocol",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's willingness or ability to comply with study procedures."
          },
          {
            "text": "The guardian of the subject and the subject of independent informed age are willing and able to provide written informed consent to participate in the study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about informed consent capacity or willingness provided in vignette."
          },
          {
            "text": "The subject is known to be allergic to any azole antifungal therapy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of azole antifungal allergy mentioned in patient's medical history."
          },
          {
            "text": "The subject is known to be allergic to other ingredients contained in the study drug",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about allergies to other study drug ingredients."
          },
          {
            "text": "The researcher believes that the condition of the child may interfere with study participation or other inappropriate conditions",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Researcher's clinical judgment regarding interference with study participation not documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: patient is 45 years old; trial restricted to ages 0-18 years."
      },
      {
        "nct_id": "NCT07654647",
        "title": "Clinical Evaluation of Patient-Specific 3D-Printed Titanium Implants for Facial Reconstruction.",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 18 years or older",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "45-year-old man",
            "reasoning": "Patient is 45 years old, which meets the age threshold of 18 or older."
          },
          {
            "text": "Presence of facial bone defects resulting from cystic or tumoral osteolytic lesions",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Black necrotic eschar on the nasal mucosa",
            "reasoning": "Patient has necrotic tissue from rhinocerebral mucormycosis, not cystic or tumoral osteolytic lesions."
          },
          {
            "text": "Acquired or congenital facial deformities associated with bony defects or facial asymmetry",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about baseline facial asymmetry or bony defects prior to acute illness."
          },
          {
            "text": "Patients requiring patient-specific 3D-printed titanium implants for maxillofacial reconstruction",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of whether patient requires or is being planned for titanium implants."
          },
          {
            "text": "Aesthetic indications requiring custom facial implant design, including microgenia (chin retrusion)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No baseline documentation of microgenia or other aesthetic indications requiring implants."
          },
          {
            "text": "Ability to provide written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient's cognitive and legal capacity to consent not documented in vignette."
          },
          {
            "text": "Active pathological lesions at the time of enrollment",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Fever, facial pain, black necrotic eschar on the nasal mucosa, and periorbital swelling",
            "reasoning": "Patient presents with acute pathological lesions (mucormycosis) at presentation, meeting exclusion criterion."
          },
          {
            "text": "History of radiotherapy within 12 months prior to enrollment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of radiotherapy documented in vignette."
          },
          {
            "text": "Chronic untreated vitamin D deficiency",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vitamin D status not mentioned or assessed in available clinical information."
          },
          {
            "text": "Uncontrolled diabetes mellitus",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Poorly controlled type 2 diabetes",
            "reasoning": "Patient has uncontrolled diabetes mellitus as explicitly stated in presentation."
          },
          {
            "text": "Inability or unwillingness to comply with follow-up requirements",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient's willingness and ability to comply with follow-up not documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: active pathological lesions (necrotic eschar) and uncontrolled diabetes mellitus at enrollment; trial requires controlled diabetes and healed lesions."
      }
    ],
    "questions": [
      {
        "field": "Mucormycosis diagnosis confirmation status",
        "question": "Has mucormycosis been confirmed by histopathology, culture, or PCR from tissue or fluid samples?",
        "why": "Confirms invasive mucormycosis diagnosis required for trial enrollment; affects 3 trials."
      },
      {
        "field": "Informed consent capacity and willingness",
        "question": "Is the patient cognitively able to understand trial requirements and willing to participate, or is a legal guardian needed?",
        "why": "Essential for valid enrollment; affects 5 trial criteria and protocol compliance."
      },
      {
        "field": "Drug allergies and tolerability",
        "question": "Does the patient have any allergies to azole antifungals (fluconazole, itraconazole, posaconazole) or known intolerances?",
        "why": "Rules out contraindications to standard mucormycosis therapy used in trials."
      }
    ],
    "reeval": {
      "extended_record": "Patient presents with acute rhinocerebral mucormycosis. Nasal endoscopy and biopsy of the black necrotic eschar on the left nasal septum was performed. Histopathology confirmed wide, non-septate hyphae consistent with Mucorales species. Fungal culture grew Rhizopus oryzae. Patient remains alert and oriented to person, place, and time with intact cognition; capable of understanding informed consent requirements and has verbally agreed to participate in clinical trials. Past medical history reviewed: no documented allergies to fluconazole, itraconazole, or posaconazole. Patient denies prior azole antifungal exposure. However, patient reports severe itching and urticaria after receipt of amphotericin B liposomal on hospital day 2; reaction resolved with antihistamine. Currently on day 8 of liposomal amphotericin B therapy with adequate tolerance. Blood glucose remains elevated at 385 mg/dL despite insulin therapy. Endocrinology consulted for diabetes optimization.",
      "answers": [
        {
          "question": "Has mucormycosis been confirmed by histopathology, culture, or PCR from tissue or fluid samples?",
          "answer": "Yes, confirmed by both histopathology and culture. Biopsy of nasal eschar showed wide, non-septate hyphae consistent with Mucorales, and fungal culture grew Rhizopus oryzae.",
          "evidence_quote": "Nasal endoscopy and biopsy of the black necrotic eschar on the left nasal septum was performed. Histopathology confirmed wide, non-septate hyphae consistent with Mucorales species. Fungal culture grew Rhizopus oryzae."
        },
        {
          "question": "Is the patient cognitively able to understand trial requirements and willing to participate, or is a legal guardian needed?",
          "answer": "Patient is cognitively intact, alert and oriented to person, place, and time, capable of understanding informed consent, and has verbally agreed to participate in clinical trials. No legal guardian is needed.",
          "evidence_quote": "Patient remains alert and oriented to person, place, and time with intact cognition; capable of understanding informed consent requirements and has verbally agreed to participate in clinical trials."
        },
        {
          "question": "Does the patient have any allergies to azole antifungals (fluconazole, itraconazole, posaconazole) or known intolerances?",
          "answer": "No documented allergies to fluconazole, itraconazole, or posaconazole. Patient denies prior azole antifungal exposure. However, patient had a reaction to amphotericin B (urticaria and itching).",
          "evidence_quote": "no documented allergies to fluconazole, itraconazole, or posaconazole. Patient denies prior azole antifungal exposure. However, patient reports severe itching and urticaria after receipt of amphotericin B liposomal on hospital day 2"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT07339800",
          "criterion": "With a diagnosis of probable or proven invasive pulmonary infection with Mucorales according to the 2020 EORTC/MSGERC criteria",
          "before": "UNCERTAIN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07339800",
          "criterion": "No diagnosis of probable or proven invasive pulmonary infection with Mucorales according to EORTC/MSGERC 2020 criteria",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05406037",
          "criterion": "Informed consent obtained from participant or parent/guardian for children",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05406037",
          "criterion": "For case group: diagnosis of mucormycosis confirmed by conventional mycology data and/or positivity of q-PCR and/or anatomopathologic diagnosis with compatible clinical situation",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06440915",
          "criterion": "The subject and his/her guardian are willing to comply with the procedures and operations specified in the study protocol",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        },
        {
          "nct_id": "NCT06440915",
          "criterion": "The guardian of the subject and the subject of independent informed age are willing and able to provide written informed consent to participate in the study",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        },
        {
          "nct_id": "NCT06440915",
          "criterion": "The subject is known to be allergic to any azole antifungal therapy",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06440915",
          "criterion": "The subject is known to be allergic to other ingredients contained in the study drug",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        },
        {
          "nct_id": "NCT07654647",
          "criterion": "Ability to provide written informed consent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07654647",
          "criterion": "Inability or unwillingness to comply with follow-up requirements",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT05406037",
          "rank": 1,
          "eligibility": "INELIGIBLE",
          "rationale": "Rhinocerebral mucormycosis suspected, but trial requires either pre-transplant assessment or disseminated candidiasis/invasive aspergillosis; neither criterion met."
        },
        {
          "nct_id": "NCT07339800",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires proven/probable invasive pulmonary mucormycosis by EORTC/MSGERC 2020 criteria; patient has rhinocerebral disease, not pulmonary."
        },
        {
          "nct_id": "NCT06440915",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial restricts enrollment to ages 0–18 years; patient is 45 years old."
        },
        {
          "nct_id": "NCT07654647",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: active mucormycotic infection and uncontrolled diabetes mellitus both contraindicate enrollment; facial reconstruction not currently indicated."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S007",
    "patient_text": "A 3-month-old infant with projectile non-bilious vomiting after feeding, visible peristalsis, and a palpable olive-shaped mass in the epigastrium. Labs show hypochloremic, hypokalemic metabolic alkalosis.",
    "extraction": [
      {
        "name": "Age",
        "value": "3 months old",
        "evidence_quote": "A 3-month-old infant"
      },
      {
        "name": "Vomiting character",
        "value": "projectile non-bilious",
        "evidence_quote": "projectile non-bilious vomiting"
      },
      {
        "name": "Vomiting timing",
        "value": "after feeding",
        "evidence_quote": "vomiting after feeding"
      },
      {
        "name": "Physical exam - peristalsis",
        "value": "visible peristalsis",
        "evidence_quote": "visible peristalsis"
      },
      {
        "name": "Physical exam - abdominal mass",
        "value": "palpable olive-shaped mass in the epigastrium",
        "evidence_quote": "palpable olive-shaped mass in the epigastrium"
      },
      {
        "name": "Electrolyte abnormality 1",
        "value": "hypochloremic",
        "evidence_quote": "hypochloremic"
      },
      {
        "name": "Electrolyte abnormality 2",
        "value": "hypokalemic",
        "evidence_quote": "hypokalemic"
      },
      {
        "name": "Acid-base status",
        "value": "metabolic alkalosis",
        "evidence_quote": "metabolic alkalosis"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT05535361",
        "title": "A Feasibility Study to Evaluate Safety and Probable Benefit of the Eclipse XL1 System for Distraction Enterogenesis in Adult and Pediatric Patients With Short Bowel Syndrome",
        "phase": "NA",
        "criteria": [
          {
            "text": "Subject has short bowel syndrome, defined as 50% or less of expected bowel length based on subject age and/or height, and measured at the time of the subject's prior intestinal resection.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior bowel resection or intestinal length measurements documented in vignette."
          },
          {
            "text": "Minimum residual bowel length of 3 cm.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No bowel length measurements provided; clinical presentation suggests pyloric stenosis, not short bowel."
          },
          {
            "text": "Male or female patients aged 3 months to 65 years inclusive.",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 3 months old",
            "reasoning": "Patient is 3 months old, within the 3 months to 65 years inclusive range."
          },
          {
            "text": "The subject, parent or legal guardian of the subject is able to read, understand, and is willing to provide informed consent.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about parent/guardian's ability to read, understand, or consent."
          },
          {
            "text": "The subject or parent or legal guardian of the patient is able to understand the requirements of the study and is willing to bring the subject to all clinic visits and complete all study related procedures.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about parent/guardian's ability or willingness to comply with study requirements."
          },
          {
            "text": "Ultra-short bowel syndrome defined as less than 3 cm of bowel length.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No bowel length measurements provided to assess ultra-short bowel syndrome status."
          },
          {
            "text": "Diagnosed Inflammatory bowel disease-unclassified (not Crohn's or ulcerative colitis).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of inflammatory bowel disease-unclassified diagnosis."
          },
          {
            "text": "Evidence of active or prior Crohn's disease.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of Crohn's disease; clinical picture consistent with pyloric stenosis."
          },
          {
            "text": "Primary intestinal failure (i.e., without loss or resection of intestinal tissue).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of intestinal resection or primary intestinal failure history."
          },
          {
            "text": "Coagulopathy, as defined by INR > 1.4 or platelets < 100.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No INR or platelet count data provided in vignette."
          },
          {
            "text": "Known immunocompromised status including individuals who have undergone organ transplantation, chemotherapy or radiotherapy within the past 12 months, who have clinically significant leukopenia, who are positive for human immunodeficiency virus (HIV), or whose immune status makes the subject a poor candidate for clinical trial participation in the opinion of the Investigator.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about immunocompromised status, transplantation, chemotherapy, radiotherapy, leukopenia, or HIV."
          },
          {
            "text": "Subject is determined by the investigator to be unsuitable for participation in this trial for any reason.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Investigator's discretionary judgment cannot be determined from clinical record."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Clinical presentation suggests pyloric stenosis, not short bowel syndrome. Eligibility for short bowel syndrome and bowel length criteria cannot be assessed."
      },
      {
        "nct_id": "NCT06031025",
        "title": "Prevalence and Natural History of Functional Gastrointestinal Disorders Among At-risk Infants.",
        "phase": "NA",
        "criteria": [
          {
            "text": "Gestational age at birth < 31 weeks",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Gestational age at birth not provided in vignette."
          },
          {
            "text": "Gestational age at birth < 37 weeks with major respiratory or neurologic morbidity",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Gestational age and perinatal morbidity history not documented."
          },
          {
            "text": "History of perinatal asphyxia",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about perinatal asphyxia in vignette."
          },
          {
            "text": "Lack of informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Informed consent status not mentioned in clinical record."
          },
          {
            "text": "Diagnosis of congenital gastrointestinal disease",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "projectile non-bilious vomiting, visible peristalsis, palpable olive-shaped mass in the epigastrium, hypochloremic hypokalemic metabolic alkalosis",
            "reasoning": "Clinical presentation and findings are pathognomonic for pyloric stenosis, a congenital GI disease."
          },
          {
            "text": "Diagnosis of inflammatory bowel disease",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "3-month-old infant with projectile vomiting and olive-shaped epigastric mass",
            "reasoning": "Clinical picture indicates pyloric stenosis, not inflammatory bowel disease."
          },
          {
            "text": "Diagnosis of gastrointestinal cancer",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "3-month-old infant with pyloric stenosis findings",
            "reasoning": "No evidence of GI malignancy; presentation consistent with benign congenital pyloric stenosis."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Excluded: congenital gastrointestinal disease (pyloric stenosis) is an explicit exclusion criterion."
      },
      {
        "nct_id": "NCT04515251",
        "title": "Ultrasound Evaluation of Superior Mesenteric Artery Measurements in a Healthy Pediatric Population",
        "phase": "NA",
        "criteria": [
          {
            "text": "Male and female children",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Sex/gender not specified in vignette; cannot determine if male or female."
          },
          {
            "text": "Age ranging from 10 to 15 years, included",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 3 months old",
            "reasoning": "Patient is 3 months old; criterion requires 10-15 years old."
          },
          {
            "text": "Abdominal ultrasound examination to be performed for indications other than gastrointestinal evaluation",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about whether ultrasound was performed or its indications."
          },
          {
            "text": "Signed Informed Consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about consent status in vignette."
          },
          {
            "text": "Presence of a disease that could distort the anatomy around the SMA (e.g., abdominal mass, lymphadenopathy, severe scoliosis, free abdominal fluid)",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "palpable olive-shaped mass in the epigastrium",
            "reasoning": "Patient has abdominal mass (olive-shaped mass consistent with pyloric stenosis), meeting exclusion criterion."
          },
          {
            "text": "Oncologic patients at risk of neoplastic cachexia",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about oncologic diagnosis or neoplastic cachexia risk."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: patient is 3 months old, trial requires ages 10-15 years. Pyloric mass meets SMA-distorting anatomy exclusion."
      },
      {
        "nct_id": "NCT06687564",
        "title": "Role of ACTG2 Variants in Smooth Muscle Determination and Function in Pediatric Intestinal Pseudo-obstruction.",
        "phase": "NA",
        "criteria": [
          {
            "text": "Minor or adult patient ≥ 4 years of age",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 3 months old",
            "reasoning": "Patient is 3 months old, criterion requires ≥4 years of age."
          },
          {
            "text": "Patient with PIPO before age 18",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "3-month-old infant with projectile non-bilious vomiting, visible peristalsis, palpable olive-shaped mass",
            "reasoning": "Clinical presentation strongly suggests pyloric stenosis, but PIPO diagnosis not explicitly stated in vignette."
          },
          {
            "text": "Patient with PIPO meeting at least 2 of the ESPGHAN criteria (Thapar et al 2018)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "ESPGHAN criteria for PIPO not detailed in vignette; cannot assess met criteria count."
          },
          {
            "text": "Carrying the R178, R257, R40 or A136 mutation of the ACTG2 gene",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No genetic testing or ACTG2 mutation status documented in vignette."
          },
          {
            "text": "Patient whose assent has been obtained and whose legal guardians have given their written informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Consent status not mentioned in clinical vignette."
          },
          {
            "text": "Patient affiliated to the French Social Security system or benefiting from an equivalent plan",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Social security or insurance affiliation not documented in vignette."
          },
          {
            "text": "Patients with a history of radiotherapy treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of radiotherapy mentioned in vignette."
          },
          {
            "text": "Patient with lymphocyte lineage damage",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No lymphocyte lineage damage or hematologic conditions documented."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: patient is 3 months old, trial requires age ≥4 years. Presentation consistent with pyloric stenosis, not primary intestinal pseudo-obstruction."
      }
    ],
    "questions": [
      {
        "field": "Informed consent and enrollment status",
        "question": "Are the parents willing and able to provide informed consent and participate in a clinical trial?",
        "why": "Prerequisite for all trial enrollment; affects 4 criteria"
      },
      {
        "field": "Prior intestinal surgery and bowel length",
        "question": "Has this infant had any abdominal surgery, bowel resection, or measurement of remaining bowel length?",
        "why": "Determines short bowel syndrome eligibility; excludes from multiple trials"
      },
      {
        "field": "Birth history and perinatal complications",
        "question": "What was the gestational age at birth, and were there any perinatal complications or birth trauma?",
        "why": "Critical for NCT06031025 eligibility and determines inclusion in age-specific criteria"
      }
    ],
    "reeval": {
      "extended_record": "3-month-old male presenting with classic infantile hypertrophic pyloric stenosis (IHPS). Projectile non-bilious vomiting observed after each feeding for 2 weeks. Physical examination confirms visible peristaltic waves and firm olive-shaped mass palpable in the epigastrium. Laboratory studies reveal hypochloremic, hypokalemic metabolic alkalosis: serum chloride 94 mEq/L (normal 98-107), potassium 3.1 mEq/L (normal 3.5-5.0), pH 7.52 with HCO3 32 mEq/L. Abdominal ultrasound shows pyloric muscle thickness of 4.2 mm with pyloric channel length of 16 mm, confirming diagnosis. No prior abdominal surgery or bowel resection. Infant born at 38 weeks gestation via uncomplicated spontaneous vaginal delivery with Apgar scores 8 and 9 at 1 and 5 minutes, respectively. No birth trauma or perinatal complications documented. Parents are English-speaking, college-educated, and have explicitly consented to participate in the clinical trial evaluating minimally invasive pyloromyotomy techniques.",
      "answers": [
        {
          "question": "Are the parents willing and able to provide informed consent and participate in a clinical trial?",
          "answer": "Yes, the parents are willing and able to provide informed consent and participate in the clinical trial.",
          "evidence_quote": "Parents are English-speaking, college-educated, and have explicitly consented to participate in the clinical trial evaluating minimally invasive pyloromyotomy techniques."
        },
        {
          "question": "Has this infant had any abdominal surgery, bowel resection, or measurement of remaining bowel length?",
          "answer": "No, the infant has not had any prior abdominal surgery or bowel resection, and no bowel length measurement has been performed.",
          "evidence_quote": "No prior abdominal surgery or bowel resection."
        },
        {
          "question": "What was the gestational age at birth, and were there any perinatal complications or birth trauma?",
          "answer": "The infant was born at 38 weeks gestation with an uncomplicated delivery (Apgar scores 8 and 9 at 1 and 5 minutes) and no perinatal complications or birth trauma.",
          "evidence_quote": "Infant born at 38 weeks gestation via uncomplicated spontaneous vaginal delivery with Apgar scores 8 and 9 at 1 and 5 minutes, respectively. No birth trauma or perinatal complications documented."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06031025",
          "criterion": "Gestational age at birth < 31 weeks",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "Gestational age at birth < 37 weeks with major respiratory or neurologic morbidity",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "History of perinatal asphyxia",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06031025",
          "criterion": "Lack of informed consent",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT04515251",
          "criterion": "Signed Informed Consent",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06687564",
          "criterion": "Patient whose assent has been obtained and whose legal guardians have given their written informed consent",
          "before": "UNKNOWN",
          "after": "UNCERTAIN"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT05535361",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Clinical presentation suggests pyloric stenosis, not short bowel syndrome. Short bowel syndrome status and residual bowel length unknown; eligibility cannot be determined."
        },
        {
          "nct_id": "NCT06031025",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: trial requires gestational age <31 weeks or <37 weeks with major morbidity/perinatal asphyxia; patient lacks these risk factors."
        },
        {
          "nct_id": "NCT04515251",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient age 3 months does not meet inclusion criterion of 10-15 years; palpable epigastric mass may distort SMA anatomy."
        },
        {
          "nct_id": "NCT06687564",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient age 3 months does not meet inclusion criterion of ≥4 years; clinical picture consistent with pyloric stenosis, not PIPO."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S008",
    "patient_text": "A 60-year-old woman presents with progressive dyspnea, dry cough, and clubbing of the fingers. Chest CT reveals bilateral basal reticular opacities with honeycombing.",
    "extraction": [
      {
        "name": "Age",
        "value": "60",
        "evidence_quote": "A 60-year-old woman"
      },
      {
        "name": "Sex",
        "value": "Female",
        "evidence_quote": "A 60-year-old woman"
      },
      {
        "name": "Chief complaint/Symptom 1",
        "value": "Progressive dyspnea",
        "evidence_quote": "progressive dyspnea"
      },
      {
        "name": "Chief complaint/Symptom 2",
        "value": "Dry cough",
        "evidence_quote": "dry cough"
      },
      {
        "name": "Physical exam finding",
        "value": "Clubbing of the fingers",
        "evidence_quote": "clubbing of the fingers"
      },
      {
        "name": "Imaging modality",
        "value": "Chest CT",
        "evidence_quote": "Chest CT"
      },
      {
        "name": "Imaging finding 1",
        "value": "Bilateral basal reticular opacities",
        "evidence_quote": "bilateral basal reticular opacities"
      },
      {
        "name": "Imaging finding 2",
        "value": "Honeycombing",
        "evidence_quote": "honeycombing"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT07299695",
        "title": "Intravenous Immunoglobulin for the Treatment of Acute Exacerbations of Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Patients ≥ 18 years of age",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "A 60-year-old woman",
            "reasoning": "Patient is 60 years old, which meets the ≥18 years requirement."
          },
          {
            "text": "Patients with IPF diagnosis that fulfils ATS/ERS Consensus Criteria",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Bilateral basal reticular opacities with honeycombing",
            "reasoning": "CT findings suggest IPF, but clinical diagnosis per ATS/ERS criteria requires additional criteria beyond imaging (PFT data, exclusion of other diagnoses) not provided."
          },
          {
            "text": "Patients hospitalised with a definite or suspected AE-IPF diagnosis, as defined by the international working group criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about hospitalization status or acute exacerbation diagnosis."
          },
          {
            "text": "Patient able to understand and sign a written informed consent form, or consent signed by legally authorized representative",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient's capacity to consent or legal representation status."
          },
          {
            "text": "Patients with acute worsening due to uncontrolled heart failure or pulmonary embolism",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No clinical information about heart failure, pulmonary embolism, or acute worsening cause."
          },
          {
            "text": "Patients with known hypersensitivity to corticosteroids, IVIG or any component of the study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented history of hypersensitivity to corticosteroids, IVIG, or study components."
          },
          {
            "text": "Patients with known IgA deficiency (IgA level <7 mg/dL)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No IgA level laboratory values documented in vignette."
          },
          {
            "text": "Patients with active malignancy or currently receiving cancer treatment, except for basal cell or squamous cell skin cancer or low-risk prostate cancer (T1 or T2a stage with PSA <10 ng/dL)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about active malignancy or current cancer treatment status."
          },
          {
            "text": "Patients that have received treatment for >14 days within the preceding month with >20mg daily prednisone (or equivalent) or any treatment during the last month with immunosuppressants or >1 mg/kg/d from more than 7 days in the last 15 days",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documentation of recent corticosteroid or immunosuppressant treatment history."
          },
          {
            "text": "Patients participating in another interventional clinical trial",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about participation in other clinical trials."
          },
          {
            "text": "Patients with documented pregnancy or lactation",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "A 60-year-old woman",
            "reasoning": "At age 60, pregnancy and lactation are highly unlikely; criterion statement is false."
          },
          {
            "text": "Patients under tutorship, curatorship, deprived of liberty, or under court protection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about legal status or guardianship."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Clinical presentation consistent with IPF (honeycombing, clubbing, dyspnea); requires confirmation of acute exacerbation criteria and hospitalization status."
      },
      {
        "nct_id": "NCT05674994",
        "title": "Glucocorticoids Versus Placebo for the Treatment of Acute Exacerbation of Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE3",
        "criteria": [
          {
            "text": "Patient is ≥ 18 years of age",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "A 60-year-old woman",
            "reasoning": "Patient is 60 years old, which is ≥18 years of age."
          },
          {
            "text": "IPF or IPF (likely) diagnosis defined on 2018 international recommendations",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Bilateral basal reticular opacities with honeycombing",
            "reasoning": "Imaging findings consistent with IPF, but clinical diagnosis per 2018 criteria requires additional assessment not fully documented."
          },
          {
            "text": "Definite or suspected Acute Exacerbation defined by the international working group criteria after exclusion of alternative diagnoses of acute worsening",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about acute exacerbation or baseline IPF diagnosis provided in vignette."
          },
          {
            "text": "For women of childbearing age: efficient contraception for the duration of the study (defined as any contraceptive method that is used consistently and appropriately and has a low failure rate of less than 1% per year)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient is 60 years old; childbearing age status and contraception use not documented."
          },
          {
            "text": "Affiliation to the social security",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about social security affiliation provided."
          },
          {
            "text": "Identified etiology for acute worsening (i.e.: infectious disease)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about alternative diagnoses for acute worsening documented."
          },
          {
            "text": "Known hypersensitivity to glucocorticoids or to any component of the study treatment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No documented history of glucocorticoid hypersensitivity."
          },
          {
            "text": "Patient requiring mechanical ventilation or already on mechanical ventilation",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about mechanical ventilation status documented."
          },
          {
            "text": "Active bacterial, viral, fungal or parasitic infection (SARS-CoV-2, Influenzae A, Influenzae B and Respiratory Syncytial Virus are considered active viral infections)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about active infections documented."
          },
          {
            "text": "Active cancer",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about active cancer documented."
          },
          {
            "text": "Patient on a lung transplantation waiting list",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about lung transplantation waiting list status."
          },
          {
            "text": "Treatment with glucocorticoids > 1 mg/kg/d from more than 7 days in the last 15 days",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about current glucocorticoid dosing or duration."
          },
          {
            "text": "Documented pregnancy or lactation",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "60-year-old woman",
            "reasoning": "Patient is postmenopausal age; pregnancy and lactation are not applicable."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Imaging findings suggest IPF; acute exacerbation status and alternative diagnoses must be excluded; contraception requirements apply if childbearing age."
      },
      {
        "nct_id": "NCT07447102",
        "title": "Phase II Clinical Study of BC006 in Patients With Idiopathic Pulmonary Fibrosis",
        "phase": "PHASE2",
        "criteria": [
          {
            "text": "Must provide written informed consent form (ICF) indicating understanding of the study and voluntary participation.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about informed consent status."
          },
          {
            "text": "Aged ≥40 years at the time of signing the ICF.",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 60",
            "reasoning": "Patient is 60 years old, which meets the ≥40 years requirement."
          },
          {
            "text": "Diagnosis of idiopathic pulmonary fibrosis (IPF) according to the 2022 ATS/ERS/JRS/ALAT clinical practice guideline.",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Progressive dyspnea, dry cough, clubbing, bilateral basal reticular opacities with honeycombing",
            "reasoning": "Clinical presentation and imaging suggest IPF but diagnosis not explicitly confirmed per 2022 guidelines."
          },
          {
            "text": "HRCT pattern consistent with usual interstitial pneumonia (UIP) or probable UIP for IPF confirmed by independent central imaging review, or if HRCT shows indeterminate UIP, diagnosis of IPF must be confirmed by histopathology from prior lung biopsy.",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Chest CT reveals bilateral basal reticular opacities with honeycombing",
            "reasoning": "Pattern consistent with UIP but independent central imaging review and histopathology confirmation status unknown."
          },
          {
            "text": "Forced vital capacity percent predicted (FVC% predicted) ≥45% during the screening period.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No FVC% predicted value provided in vignette."
          },
          {
            "text": "Diffusing capacity of the lung for carbon monoxide percent predicted (DLCO% predicted), corrected for hemoglobin, ≥30% and ≤90% during the screening period.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No DLCO% predicted value provided in vignette."
          },
          {
            "text": "Either on stable dose of nintedanib (≥100 mg BID) or pirfenidone (≥400 mg TID) for ≥8 weeks prior to screening with no dose changes, or treatment-naïve or discontinued for ≥4 weeks prior to screening with no plans to initiate during study.",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about prior or current antifibrotic therapy provided."
          },
          {
            "text": "Interstitial lung disease of known etiology (e.g., domestic and occupational environmental exposures, connective tissue disease, drug toxicity).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about etiology or potential known exposures/connective tissue disease."
          },
          {
            "text": "Other pulmonary diseases considered clinically significant by the investigator (e.g., asthma, chronic obstructive pulmonary disease, cavitary or pleural disease).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about asthma, COPD, cavitary disease, or pleural involvement."
          },
          {
            "text": "Emphysema ≥50%, or emphysema greater than fibrosis, as determined by independent central imaging review of HRCT.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Emphysema percentage not quantified in imaging report."
          },
          {
            "text": "Acute exacerbation of IPF within 3 months prior to screening or during the screening period.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about acute exacerbation history or timing."
          },
          {
            "text": "Sustained improvement in IPF severity within 12 months prior to screening or during the screening period, as judged by investigator based on changes in FVC, DLCO, and/or chest HRCT scan.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No longitudinal data on FVC, DLCO, or prior imaging changes provided."
          },
          {
            "text": "Pre-bronchodilator forced expiratory volume in 1 second (FEV1)/FVC <0.70 during the screening period.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No FEV1/FVC ratio provided in vignette."
          },
          {
            "text": "Known increase in FEV1 and/or FVC ≥12% and ≥200 mL post-bronchodilator.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No post-bronchodilator spirometry data provided."
          },
          {
            "text": "History of smoking within 3 months prior to screening or during the screening period, or inability to refrain from smoking for the duration of the study.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No smoking history information provided in vignette."
          },
          {
            "text": "Acute exacerbation of IPF within 3 months prior to screening or during the screening period, as judged by the investigator.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about acute exacerbation within 3 months."
          },
          {
            "text": "History of severe cardiovascular or cerebrovascular disease, including ventricular arrhythmia requiring clinical intervention, uncontrolled atrial arrhythmia, congestive heart failure NYHA Class ≥III, LVEF <35%, uncontrolled hypertension (systolic ≥160 mmHg or diastolic ≥100 mmHg), or acute coronary syndrome/stroke/TIA within 6 months prior to screening.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No cardiovascular or cerebrovascular history provided."
          },
          {
            "text": "Current or suspected malignancy, or history of malignancy within 5 years prior to screening (excluding basal cell carcinoma, squamous cell carcinoma of skin, superficial bladder cancer, or carcinoma in situ with curative treatment).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No malignancy history information provided."
          },
          {
            "text": "Active hepatitis B (positive HBsAg and HBV DNA >ULN) or active hepatitis C (positive HCV-Ab and HCV RNA >ULN).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No hepatitis serology data provided."
          },
          {
            "text": "Positive interferon-γ release assay for tuberculosis during screening (unless completed tuberculosis treatment within 6 months prior to screening with no evidence of recurrence).",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No tuberculosis screening results provided."
          },
          {
            "text": "Prior treatment with a highly selective small-molecule CSF-1R inhibitor (excluding nintedanib) or anti-CSF-1/CSF-1R antibody.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No prior treatment history with CSF-1R inhibitors provided."
          },
          {
            "text": "Received systemic corticosteroid therapy with prednisone >15 mg/day or equivalent within 4 weeks prior to screening or during the screening period.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about systemic corticosteroid dosing provided."
          },
          {
            "text": "Pregnant or lactating female, or female of childbearing potential with positive serum pregnancy test within 7 days prior to first dose of study drug.",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Female patient but pregnancy status not documented."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 3,
        "rationale": "CT pattern consistent with IPF; diagnosis confirmed by imaging findings; central imaging review or prior histology needed for enrollment."
      },
      {
        "nct_id": "NCT03297775",
        "title": "Rheumatoid Arthritis Patients at Risk for Interstitial Lung Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "≥ 45 years old",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 60",
            "reasoning": "Patient is 60 years old, which meets the ≥45 years criterion."
          },
          {
            "text": "Diagnosis of RA using the 2010 American College of Rheumatology (ACR) criteria",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about RA diagnosis or ACR criteria assessment in vignette."
          },
          {
            "text": "Ability to give informed consent",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient's capacity or ability to provide informed consent."
          },
          {
            "text": "Inability to give informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about patient's capacity or inability to provide informed consent."
          },
          {
            "text": "Pregnant women",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "A 60-year-old woman",
            "reasoning": "Patient is postmenopausal; no indication of pregnancy."
          },
          {
            "text": "History of interstitial lung disease",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "bilateral basal reticular opacities with honeycombing",
            "reasoning": "Imaging findings are consistent with interstitial lung disease, satisfying this exclusion."
          },
          {
            "text": "Evidence of other causes of diffuse parenchymal lung disease such as infection, drug toxicity, other autoimmune processes",
            "type": "exclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Progressive dyspnea, dry cough, clubbing, bilateral basal reticular opacities with honeycombing",
            "reasoning": "Clinical presentation suggests ILD but underlying etiology not definitively established; could be autoimmune, infectious, or other."
          },
          {
            "text": "Age over 90 years old",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Age: 60",
            "reasoning": "Patient is 60 years old, which does not exceed 90 years."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: established interstitial lung disease; trial enrolls RA patients at risk for ILD, not those with existing ILD."
      }
    ],
    "questions": [
      {
        "field": "Recent acute exacerbation or clinical changes",
        "question": "Has the patient experienced any sudden worsening of shortness of breath, fever, or new respiratory symptoms in the past 4 weeks?",
        "why": "Affects 5 trials; acute exacerbation is common IPF exclusion criterion."
      },
      {
        "field": "IPF diagnostic confirmation",
        "question": "Has a pulmonologist confirmed IPF diagnosis with high-resolution CT interpretation and/or bronchoscopy with BAL findings per ATS/ERS criteria?",
        "why": "Affects 4 trials; imaging alone insufficient for most trial enrollment."
      },
      {
        "field": "Pulmonary function tests (FVC, DLCO)",
        "question": "What are the patient's most recent FVC% predicted and DLCO% predicted values, and when were they measured?",
        "why": "Affects 4 trials; specific PFT thresholds determine eligibility for most IPF trials."
      }
    ],
    "reeval": {
      "extended_record": "Patient reports stable dyspnea on exertion with no acute exacerbations over the past 4 weeks. Denies fever, chills, or new respiratory symptoms. She remains on home oxygen at 2L/min during activity. Pulmonology evaluation completed by Dr. James Martinez on 2024-01-15 confirmed idiopathic pulmonary fibrosis diagnosis based on high-resolution CT findings of bilateral basal reticular opacities with honeycombing and usual interstitial pneumonia pattern, consistent with ATS/ERS diagnostic criteria. Bronchoscopy with bronchoalveolar lavage performed 2024-01-10 showed lymphocytic predominance (18% lymphocytes) without evidence of infection or alternative diagnosis. Pulmonary function testing from 2024-01-20 demonstrated FVC 62% predicted (1.85 L) and DLCO 48% predicted (12.1 mmol/min/kPa), consistent with moderate-stage IPF. Patient counseled on disease progression and antifibrotic therapy options.",
      "answers": [
        {
          "question": "Has the patient experienced any sudden worsening of shortness of breath, fever, or new respiratory symptoms in the past 4 weeks?",
          "answer": "No acute exacerbations; patient reports stable dyspnea on exertion with no fever, chills, or new respiratory symptoms over the past 4 weeks.",
          "evidence_quote": "Patient reports stable dyspnea on exertion with no acute exacerbations over the past 4 weeks. Denies fever, chills, or new respiratory symptoms."
        },
        {
          "question": "Has a pulmonologist confirmed IPF diagnosis with high-resolution CT interpretation and/or bronchoscopy with BAL findings per ATS/ERS criteria?",
          "answer": "Yes, pulmonologist Dr. James Martinez confirmed IPF diagnosis via high-resolution CT showing bilateral basal reticular opacities with honeycombing and usual interstitial pneumonia pattern, plus bronchoscopy with BAL demonstrating lymphocytic predominance (18%), meeting ATS/ERS criteria.",
          "evidence_quote": "Pulmonology evaluation completed by Dr. James Martinez on 2024-01-15 confirmed idiopathic pulmonary fibrosis diagnosis based on high-resolution CT findings of bilateral basal reticular opacities with honeycombing and usual interstitial pneumonia pattern, consistent with ATS/ERS diagnostic criteria. Bronchoscopy with bronchoalveolar lavage performed 2024-01-10 showed lymphocytic predominance (18% lymphocytes)"
        },
        {
          "question": "What are the patient's most recent FVC% predicted and DLCO% predicted values, and when were they measured?",
          "answer": "FVC 62% predicted (1.85 L) and DLCO 48% predicted (12.1 mmol/min/kPa), measured on 2024-01-20.",
          "evidence_quote": "Pulmonary function testing from 2024-01-20 demonstrated FVC 62% predicted (1.85 L) and DLCO 48% predicted (12.1 mmol/min/kPa)"
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT07299695",
          "criterion": "Patients with IPF diagnosis that fulfils ATS/ERS Consensus Criteria",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05674994",
          "criterion": "IPF or IPF (likely) diagnosis defined on 2018 international recommendations",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05674994",
          "criterion": "Definite or suspected Acute Exacerbation defined by the international working group criteria after exclusion of alternative diagnoses of acute worsening",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05674994",
          "criterion": "Identified etiology for acute worsening (i.e.: infectious disease)",
          "before": "UNKNOWN",
          "after": "MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT07299695",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Clinical presentation consistent with IPF; uncertain if acute exacerbation meets IWG criteria or hospitalization status known; consent ability unconfirmed."
        },
        {
          "nct_id": "NCT07447102",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Honeycombing on CT suggests UIP pattern consistent with IPF diagnosis; imaging pattern and consent status require confirmation."
        },
        {
          "nct_id": "NCT03297775",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: established interstitial lung disease history. Trial requires RA diagnosis without prior ILD."
        },
        {
          "nct_id": "NCT05674994",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: no acute exacerbation criteria met and potential infectious etiology not ruled out; chronic IPF presentation only."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S009",
    "patient_text": "A 19-year-old male presents with fever, sore throat, fatigue, and posterior cervical lymphadenopathy. Physical exam reveals splenomegaly, and a monospot test is positive.",
    "extraction": [
      {
        "name": "Age",
        "value": "19 years old",
        "evidence_quote": "A 19-year-old male"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "A 19-year-old male"
      },
      {
        "name": "Fever",
        "value": "Present",
        "evidence_quote": "presents with fever"
      },
      {
        "name": "Sore throat",
        "value": "Present",
        "evidence_quote": "sore throat"
      },
      {
        "name": "Fatigue",
        "value": "Present",
        "evidence_quote": "fatigue"
      },
      {
        "name": "Posterior cervical lymphadenopathy",
        "value": "Present",
        "evidence_quote": "posterior cervical lymphadenopathy"
      },
      {
        "name": "Splenomegaly",
        "value": "Present",
        "evidence_quote": "Physical exam reveals splenomegaly"
      },
      {
        "name": "Monospot test",
        "value": "Positive",
        "evidence_quote": "a monospot test is positive"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT06005246",
        "title": "Munich ME/CFS Cohort Study",
        "phase": "NA",
        "criteria": [
          {
            "text": "Written consent of the patient (or legal guardian for patients aged < 18 years)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not mention written consent status."
          },
          {
            "text": "Age 0 - 25 years (including)",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "A 19-year-old male",
            "reasoning": "Patient is 19 years old, within the 0-25 year range."
          },
          {
            "text": "Documented or probable acute infectious disease at the onset of ME/CFS symptoms",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "fever, sore throat, fatigue, posterior cervical lymphadenopathy, splenomegaly, monospot test is positive",
            "reasoning": "Acute infectious disease (infectious mononucleosis) documented at symptom onset."
          },
          {
            "text": "Diagnosis of ME/CFS according to the IOM criteria, the CCC, the diagnostic worksheet published by P.C. Rowe et al. (2017), or the pediatric case definition published by L.A. Jason et al. (2006)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not document ME/CFS diagnosis by specified criteria."
          },
          {
            "text": "History of drug/medication abuse",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about drug/medication abuse history."
          },
          {
            "text": "Major surgery within the last six months",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of any surgery in the past six months."
          },
          {
            "text": "Presence of organ failure",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about organ failure or functional impairment."
          },
          {
            "text": "Post-stroke or craniocerebral trauma with cognitive deficits",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of stroke, trauma, or cognitive deficits mentioned."
          },
          {
            "text": "Post-intensive care syndrome",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of intensive care unit admission or PICS."
          },
          {
            "text": "Diagnosis of syphilis, Lyme disease, AIDS, hepatitis B/C, multiple sclerosis, systemic lupus erythematosus, Sjörgren's syndrome, or malignancy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette does not document or exclude these specific diagnoses."
          },
          {
            "text": "Major depression or other severe psychiatric illness",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No psychiatric history or current mental health status documented."
          },
          {
            "text": "Primary sleep disorder",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about sleep disorders or sleep patterns."
          },
          {
            "text": "Severe endocrine disease (e.g., hypopituitarism, adrenal insufficiency)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No endocrine disease or hypopituitarism documented."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Acute EBV infection (monospot positive) does not meet ME/CFS diagnostic criteria; ME/CFS requires prolonged post-viral course. Consent status unknown."
      },
      {
        "nct_id": "NCT05778006",
        "title": "Multi-Center Registry for ME/CFS",
        "phase": "NA",
        "criteria": [
          {
            "text": "ME/CFS diagnosis (ICD-10 G93.3) based on internationally established criteria",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Monospot test positive with fever, sore throat, lymphadenopathy, and splenomegaly consistent with infectious mononucleosis, not ME/CFS.",
            "reasoning": "Clinical presentation indicates acute infectious mononucleosis, not ME/CFS diagnosis."
          },
          {
            "text": "Informed consent by patients and/or guardian(s)",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette contains no information about informed consent status or guardian availability."
          },
          {
            "text": "No ME/CFS (ICD-10 G93.3)",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Monospot test positive with acute infectious illness presentation; no ME/CFS diagnosis documented.",
            "reasoning": "Patient does not have ME/CFS diagnosis; presents with acute infectious mononucleosis instead."
          },
          {
            "text": "No informed consent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Vignette provides no information regarding informed consent documentation or discussion."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 2,
        "rationale": "Excluded: patient has acute infectious mononucleosis, not ME/CFS (ICD-10 G93.3). Trial requires established ME/CFS diagnosis."
      },
      {
        "nct_id": "NCT00032513",
        "title": "Genetic Studies of Chronic Active Epstein-Barr Disease",
        "phase": "NA",
        "criteria": [
          {
            "text": "Age 1 year old and above",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 19 years old",
            "reasoning": "Patient is 19 years old, which is 1 year and above."
          },
          {
            "text": "Severe progressive illness that began as a primary EBV infection, or associated with positive EBV-specific antibody titers (IgG-VCA, EA or EBNA) not otherwise explained",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Monospot test: Positive",
            "reasoning": "Positive monospot suggests EBV infection, but specific antibody titers (IgG-VCA, EA, EBNA) not documented."
          },
          {
            "text": "Evidence of major organ involvement such as lymphadenitis, hemophagocytosis, meningoencephalitis, persistent hepatitis, splenomegaly, interstitial pneumonitis, bone marrow hypoplasia, or uveitis",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Splenomegaly: Present; Posterior cervical lymphadenopathy: Present",
            "reasoning": "Patient has splenomegaly and lymphadenitis, both listed major organ involvement criteria."
          },
          {
            "text": "Detection of elevated levels of EBV DNA, RNA or proteins in affected tissues OR elevated levels of EBV DNA in the peripheral blood",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "EBV DNA, RNA, or protein levels not reported in clinical presentation."
          },
          {
            "text": "Children under the age of 3 years old enrolled as samples-only participants and not be evaluated at the Clinical Center",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Age: 19 years old",
            "reasoning": "Patient is 19 years old, not under 3 years old."
          },
          {
            "text": "Any other condition that, in the opinion of the investigator, would make the patient unsuitable for enrollment or could interfere with the patient participating in the study",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Requires investigator discretion and judgment about overall suitability."
          },
          {
            "text": "For relatives of CAEBV patients: age 3 years and above",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Patient relationship to CAEBV patients (relative vs unrelated) not specified."
          },
          {
            "text": "For unrelated volunteers: age 18 years and above",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Age: 19 years old",
            "reasoning": "If unrelated volunteer, patient is 18 years and above."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: trial requires either age <3 years or severe progressive EBV illness; patient has acute self-limited monospot-positive infection."
      },
      {
        "nct_id": "NCT05127980",
        "title": "Occurrence of Antibodies Cross-reacting With Autoantigens in Primary EBV Infection",
        "phase": "NA",
        "criteria": [
          {
            "text": "Informed consent as documented by signature",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about informed consent documentation in vignette."
          },
          {
            "text": "Confirmed primary EBV infection as confirmed by the treating clinician with compatible clinical symptoms including but not limited to malaise, headache, fever, tonsillitis, pharyngitis, cervical lymph nodes enlargement",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Positive monospot test with fever, sore throat, fatigue, posterior cervical lymphadenopathy, splenomegaly",
            "reasoning": "Monospot positive confirms EBV; clinical symptoms of fever, sore throat, cervical lymphadenopathy present."
          },
          {
            "text": "Compatible laboratory picture including lymphocyte count elevation, LUC cells, reactive lymphocytes in manual differential, elevated liver enzymes",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No laboratory data provided on lymphocyte count, LUC cells, differential, or liver enzymes."
          },
          {
            "text": "Serology compatible with primary EBV infection: anti-EBNA IgG negative, anti-VCA IgG negative, anti-VCA IgM positive OR anti-EBNA IgG negative, anti-VCA IgG positive, anti-VCA IgM positive",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Monospot positive but specific EBV serology panel (anti-EBNA, anti-VCA IgG, anti-VCA IgM) not provided."
          },
          {
            "text": "Clinical picture of upper respiratory tract infection including but not limited to tonsillitis/pharyngitis, malaise, headache, cough, rhinitis, cervical node enlargement (for control group)",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "Sore throat, fever, posterior cervical lymphadenopathy, fatigue (malaise equivalent)",
            "reasoning": "Patient has pharyngitis, malaise, fever, and cervical node enlargement meeting URTI criteria."
          },
          {
            "text": "Confirmed primary Cytomegalovirus (CMV) infection (for control group)",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "Monospot test positive; no mention of CMV infection",
            "reasoning": "Clinical picture and positive monospot indicate EBV, not primary CMV infection."
          },
          {
            "text": "Suspicion or diagnosis of infectious mononucleosis as per judgment of the treating clinician (control group only)",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "Positive monospot test with compatible clinical presentation",
            "reasoning": "Positive monospot and classic mononucleosis symptoms indicate infectious mononucleosis diagnosis."
          },
          {
            "text": "Immunosuppression broadly defined as primary or secondary immunodeficiency or treatment with an immunosuppressive medication including ≥ 10mg prednisone equivalent",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about immunosuppression status or immunosuppressive medications."
          },
          {
            "text": "History of autoimmune disease including but not limited to SLE, vasculitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of autoimmune disease mentioned in vignette."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: patient meets infectious mononucleosis diagnosis, which is an exclusion criterion. Trial is for CMV controls, not EBV cases."
      }
    ],
    "questions": [
      {
        "field": "History of chronic medical/psychiatric conditions",
        "question": "Have you ever been diagnosed with chronic fatigue syndrome, depression, autoimmune disease, thyroid problems, or sleep disorders?",
        "why": "Affects 5 trial criteria; common exclusionary conditions in EBV studies"
      },
      {
        "field": "EBV serology and viral markers",
        "question": "Has your doctor ordered EBV antibody tests (VCA-IgM, VCA-IgG, EBNA) or viral load testing to confirm this is a new infection?",
        "why": "Affects 3 criteria; distinguishes primary from chronic/reactivated EBV infection"
      },
      {
        "field": "Complete blood count and liver function tests",
        "question": "Have recent blood tests been done showing your white blood cell count, lymphocytes, and liver enzyme levels?",
        "why": "Confirms acute EBV infection pattern; needed for baseline trial eligibility assessment"
      }
    ],
    "reeval": {
      "extended_record": "Patient is a 19-year-old male with acute infectious mononucleosis confirmed by positive monospot test. No prior history of chronic fatigue syndrome, depression, autoimmune disease, thyroid dysfunction, or sleep disorders. EBV serology performed on 2024-01-15 demonstrates VCA-IgM 2.8 (positive), VCA-IgG 0.2 (negative), and EBNA negative, confirming acute primary EBV infection. Recent CBC from 2024-01-15 shows WBC 12,400/μL (normal), lymphocytes 68% with atypical forms noted, and platelets 185,000/μL. Comprehensive metabolic panel reveals ALT 128 U/L, AST 156 U/L, and total bilirubin 1.4 mg/dL, consistent with acute viral hepatitis. Patient reports symptom onset 5 days ago with fever peaking at 102.8°F, severe pharyngeal exudate, marked posterior cervical and axillary lymphadenopathy, and significant splenomegaly on exam. No EBV viral load testing performed as clinical presentation and serology are diagnostic. Patient counseled on supportive care, activity restriction given splenomegaly, and expected 2-4 week recovery course.",
      "answers": [
        {
          "question": "Have you ever been diagnosed with chronic fatigue syndrome, depression, autoimmune disease, thyroid problems, or sleep disorders?",
          "answer": "No prior history of these conditions reported",
          "evidence_quote": "No prior history of chronic fatigue syndrome, depression, autoimmune disease, thyroid dysfunction, or sleep disorders."
        },
        {
          "question": "Have recent blood tests been done showing your white blood cell count, lymphocytes, and liver enzyme levels?",
          "answer": "Yes, CBC and CMP performed on 2024-01-15 show WBC 12,400/μL, lymphocytes 68% with atypical forms, ALT 128 U/L, AST 156 U/L, and total bilirubin 1.4 mg/dL",
          "evidence_quote": "Recent CBC from 2024-01-15 shows WBC 12,400/μL (normal), lymphocytes 68% with atypical forms noted, and platelets 185,000/μL. Comprehensive metabolic panel reveals ALT 128 U/L, AST 156 U/L, and total bilirubin 1.4 mg/dL, consistent with acute viral hepatitis."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT06005246",
          "criterion": "Diagnosis of ME/CFS according to the IOM criteria, the CCC, the diagnostic worksheet published by P.C. Rowe et al. (2017), or the pediatric case definition published by L.A. Jason et al. (2006)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Major depression or other severe psychiatric illness",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Primary sleep disorder",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06005246",
          "criterion": "Severe endocrine disease (e.g., hypopituitarism, adrenal insufficiency)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "Compatible laboratory picture including lymphocyte count elevation, LUC cells, reactive lymphocytes in manual differential, elevated liver enzymes",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT05127980",
          "criterion": "History of autoimmune disease including but not limited to SLE, vasculitis",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT05778006",
          "rank": 1,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient has acute infectious mononucleosis, not ME/CFS diagnosis required by trial."
        },
        {
          "nct_id": "NCT05127980",
          "rank": 2,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: confirmed infectious mononucleosis triggers exclusion criterion for control group enrollment."
        },
        {
          "nct_id": "NCT00032513",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Ineligible: does not meet inclusion criteria for chronic active EBV disease; presents with acute primary infection instead."
        },
        {
          "nct_id": "NCT06005246",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: acute infectious mononucleosis does not meet ME/CFS diagnostic criteria required for enrollment."
        }
      ]
    },
    "generated_at": "2026-07-08"
  },
  {
    "patient_id": "S010",
    "patient_text": "A 73-year-old man with sudden onset of a painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters.",
    "extraction": [
      {
        "name": "Age",
        "value": "73 years old",
        "evidence_quote": "A 73-year-old man"
      },
      {
        "name": "Sex",
        "value": "Male",
        "evidence_quote": "A 73-year-old man"
      },
      {
        "name": "Symptom: Vision Loss",
        "value": "Painless, curtain-like loss of vision in the right eye",
        "evidence_quote": "sudden onset of a painless, curtain-like loss of vision in the right eye"
      },
      {
        "name": "Symptom: Flashes of Light",
        "value": "Flashes of light",
        "evidence_quote": "preceded by flashes of light"
      },
      {
        "name": "Symptom: Floaters",
        "value": "Floaters",
        "evidence_quote": "floaters"
      },
      {
        "name": "Onset",
        "value": "Sudden",
        "evidence_quote": "sudden onset"
      }
    ],
    "trials": [
      {
        "nct_id": "NCT07346560",
        "title": "1ry Versus 2ry ILM Peeling in RD",
        "phase": "NA",
        "criteria": [
          {
            "text": "Patients with uncomplicated rhegmatogenous retinal detachment",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "Painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters",
            "reasoning": "Clinical presentation highly suggestive of rhegmatogenous retinal detachment, but formal diagnosis and absence of complications unconfirmed."
          },
          {
            "text": "Proliferative vitreoretinopathy (PVR)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about presence or absence of proliferative vitreoretinopathy."
          },
          {
            "text": "Recurrent retinal detachment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of prior retinal detachment episodes mentioned in vignette."
          },
          {
            "text": "Tractional retinal detachment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Clinical presentation suggests rhegmatogenous type, but tractional etiology not explicitly ruled out."
          },
          {
            "text": "Macular hole retinal detachment",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about macular involvement or macular hole present in clinical presentation."
          },
          {
            "text": "Scleral buckling is indicated",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Whether scleral buckling is indicated requires clinical examination and investigator judgment not provided."
          },
          {
            "text": "Macular scarring",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about macular scarring status in vignette."
          },
          {
            "text": "Previous pars plana vitrectomy (PPV)",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No surgical history mentioned; prior PPV status unknown."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 1,
        "rationale": "Clinical presentation consistent with rhegmatogenous retinal detachment (sudden painless vision loss, photopsia, floaters). PVR status and recurrence history unknown; eligibility unresolved pending confirmation."
      },
      {
        "nct_id": "NCT06587945",
        "title": "Nicotinamide Riboside Oral Supplementation in Macula Off Retinal Detachment",
        "phase": "PHASE4",
        "criteria": [
          {
            "text": "Age ≥ 18 years old",
            "type": "inclusion",
            "verdict": "MET",
            "effect": "PASS",
            "evidence": "73-year-old man",
            "reasoning": "Patient is 73 years old, which meets age ≥18 requirement."
          },
          {
            "text": "Able to give informed consent and comply with all study visits and procedures",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about consent capacity or ability to comply with study procedures."
          },
          {
            "text": "Present within 10 days of macula-off retinal detachment based on patient-reported history of loss of central vision",
            "type": "inclusion",
            "verdict": "UNCERTAIN",
            "effect": "REVIEW",
            "evidence": "painless, curtain-like loss of vision in the right eye, preceded by flashes of light and floaters",
            "reasoning": "Clinical presentation suggests retinal detachment with sudden onset. Unknown if macula-off, central vision involved, or within 10-day window."
          },
          {
            "text": "Present to the hospital with a visual acuity of hand motion or better in the study eye",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No current visual acuity measurement provided in the vignette."
          },
          {
            "text": "Have had previous cataract surgery in the study eye",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No surgical history mentioned regarding cataract surgery in the right eye."
          },
          {
            "text": "Have clinical indication for standard retinal reattachment surgery by means of a pars plana vitrectomy and gas tamponade",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Diagnosis suggests retinal detachment but no statement of clinical indication for vitrectomy and gas tamponade documented."
          },
          {
            "text": "Any known significant ocular disease in the study eye (e.g., cornea opacity) which would preclude a visual acuity of at least 6/7.5 (20/25) following successful vitrectomy or limit adequate visibility of the retina",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about corneal opacity, lens disease, or other significant ocular disease in study eye."
          },
          {
            "text": "History of previous ocular surgery in the study eye other than uncomplicated cataract surgery with posterior chamber intraocular lens and intact posterior capsule or refractive surgery occurring at least 3 months prior to baseline visit",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Surgical history not provided; unable to confirm prior surgeries beyond what vignette states."
          },
          {
            "text": "Participation in other clinical trials or use of any other investigational drugs or devices within 3 months prior to study participation",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about other clinical trial participation or investigational drug/device use."
          },
          {
            "text": "Females who are pregnant or lactating and women of childbearing potential",
            "type": "exclusion",
            "verdict": "NOT_MET",
            "effect": "PASS",
            "evidence": "Male",
            "reasoning": "Patient is male; exclusion criterion applies to females only."
          },
          {
            "text": "Known hepatic disease or history of significant chronic liver disease, or known renal disease",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of hepatic or renal disease documented in vignette."
          },
          {
            "text": "History of uncontrolled hypertension",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about hypertension history or current blood pressure control."
          },
          {
            "text": "History of stroke, transient ischemic attack, or major cardiac surgery within 3 months prior to study, or current treatment for systemic infection",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of stroke, TIA, cardiac surgery, or systemic infection mentioned."
          }
        ],
        "eligibility": "UNCERTAIN",
        "rank": 2,
        "rationale": "Presentation suggests macula-off retinal detachment within probable 10-day window. Visual acuity and consent capacity require clinical assessment to confirm eligibility."
      },
      {
        "nct_id": "NCT07228091",
        "title": "Surgical Procedure Efficiency Evaluation stuDy",
        "phase": "NA",
        "criteria": [
          {
            "text": "Able to understand and sign an informed consent form (ICF) that has been approved by an ethics committee",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about patient's cognitive status or ability to consent."
          },
          {
            "text": "Planned combined phacovitrectomy procedure at one of the selected surgical sites",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about planned surgical procedures or enrollment at trial sites."
          },
          {
            "text": "Planned combined phacovitrectomy procedure with 25-gauge (G) vitrectomy tools",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about planned surgical procedures or specific gauge vitrectomy tools."
          },
          {
            "text": "Unplanned/emergency phacovitrectomy",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about whether any phacovitrectomy is planned or its emergency status."
          },
          {
            "text": "Pregnant",
            "type": "exclusion",
            "verdict": "MET",
            "effect": "FAIL",
            "evidence": "A 73-year-old man",
            "reasoning": "Patient is male; pregnancy criterion cannot apply to men."
          },
          {
            "text": "Past history of phacovitrectomy in the planned operative eye",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No past surgical history provided for the right eye."
          },
          {
            "text": "Past history of cataract in the planned operative eye",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about past cataract history in the right eye."
          },
          {
            "text": "Past history of vitrectomy in the planned operative eye",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information about past vitrectomy history in the right eye."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 3,
        "rationale": "Excluded: patient is male (trial requires pregnancy exclusion criterion met for females only). Additionally, planned combined phacovitrectomy with 25G tools not confirmed."
      },
      {
        "nct_id": "NCT07081945",
        "title": "hAM for Inferior RRD",
        "phase": "NA",
        "criteria": [
          {
            "text": "Subjects having given free and informed consent to take part in the study",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No information provided about consent status in vignette."
          },
          {
            "text": "Subjects between 18 and 70 years old",
            "type": "inclusion",
            "verdict": "NOT_MET",
            "effect": "FAIL",
            "evidence": "73-year-old man",
            "reasoning": "Patient age 73 exceeds upper limit of 70 years."
          },
          {
            "text": "Subjects suffering RRD with inferior retinal breaks between 4- and 8-o'clock within the detached area regardless of PVR grade",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Clinical presentation suggests retinal detachment, but specific location of breaks and PVR grade not documented."
          },
          {
            "text": "Subjects suffering RRD requiring retinotomy inferiorly between 4- and 8-o'clock due to severe inferior PVR or inferior retinal shortening",
            "type": "inclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Retinal detachment likely, but no details on break location, PVR severity, or retinal shortening."
          },
          {
            "text": "Subjects with RRD with only anterior retina breaks or dialysis meeting indications for scleral buckling surgery",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "Retinal detachment presumed, but anterior vs. posterior break location and surgical indication unclear."
          },
          {
            "text": "Subjects with RRD whose retinal breaks are located between the 4- and 8-o'clock positions and are not involved in the detached area",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No specific information about retinal break location relative to clock positions and detached area involvement."
          },
          {
            "text": "Subjects with pre-existing serious eye diseases including corneal ulcers, glaucoma, or uveitis",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No mention of corneal ulcers, glaucoma, or uveitis in vignette."
          },
          {
            "text": "History of epilepsy or serious psychiatric diseases",
            "type": "exclusion",
            "verdict": "UNKNOWN",
            "effect": "REVIEW",
            "evidence": null,
            "reasoning": "No history of epilepsy or psychiatric disease mentioned in vignette."
          }
        ],
        "eligibility": "INELIGIBLE",
        "rank": 4,
        "rationale": "Excluded: patient is 73 years old; trial restricts enrollment to ages 18–70. Inferior RRD location and PVR grade also unconfirmed."
      }
    ],
    "questions": [
      {
        "field": "Retinal detachment characteristics",
        "question": "Has the patient had an eye exam with imaging (OCT or ultrasound) to confirm macula involvement and identify the retinal break location?",
        "why": "Macula-on vs -off status is critical for most trial eligibility criteria."
      },
      {
        "field": "Past ocular surgery history",
        "question": "Has the patient had any prior eye surgery, including vitrectomy, cataract surgery, or LASIK/refractive procedures?",
        "why": "Prior vitrectomy or retinal surgery dramatically affects trial eligibility and surgical planning."
      },
      {
        "field": "Comorbid systemic diseases",
        "question": "Does the patient have a history of kidney disease, liver disease, heart disease, or neurological conditions?",
        "why": "Systemic comorbidities exclude patients from many clinical trials due to safety concerns."
      }
    ],
    "reeval": {
      "extended_record": "On dilated fundoscopic examination and B-scan ultrasound performed 2 days after symptom onset, a superior nasal retinal break measuring approximately 2 mm was identified at 11 o'clock position with shallow superior detachment extending toward the macula. OCT imaging confirmed foveal involvement with central macular thickness of 450 micrometers and subfoveal fluid accumulation. The patient reported cataract extraction with posterior chamber IOL placement in the right eye 8 years ago and LASIK refractive surgery 15 years prior. He denied prior vitrectomy. Medical history includes well-controlled hypertension treated with lisinopril 10 mg daily and atorvastatin 20 mg daily for hyperlipidemia. Serum creatinine is 1.1 mg/dL with normal renal function. Liver function tests (AST, ALT, bilirubin) are within normal limits. Echocardiography from 2 years ago showed preserved ejection fraction at 55% with no valvular disease. Patient denies neurological symptoms or prior stroke. No dementia or Parkinson disease reported.",
      "answers": [
        {
          "question": "Has the patient had an eye exam with imaging (OCT or ultrasound) to confirm macula involvement and identify the retinal break location?",
          "answer": "Yes. B-scan ultrasound identified a superior nasal retinal break at 11 o'clock position measuring 2 mm with shallow superior detachment. OCT confirmed foveal involvement with subfoveal fluid accumulation and central macular thickness of 450 micrometers.",
          "evidence_quote": "B-scan ultrasound performed 2 days after symptom onset, a superior nasal retinal break measuring approximately 2 mm was identified at 11 o'clock position with shallow superior detachment extending toward the macula. OCT imaging confirmed foveal involvement with central macular thickness of 450 micrometers and subfoveal fluid accumulation."
        },
        {
          "question": "Has the patient had any prior eye surgery, including vitrectomy, cataract surgery, or LASIK/refractive procedures?",
          "answer": "Yes. The patient had cataract extraction with posterior chamber IOL placement in the right eye 8 years ago and LASIK refractive surgery 15 years prior. He denied prior vitrectomy.",
          "evidence_quote": "The patient reported cataract extraction with posterior chamber IOL placement in the right eye 8 years ago and LASIK refractive surgery 15 years prior. He denied prior vitrectomy."
        },
        {
          "question": "Does the patient have a history of kidney disease, liver disease, heart disease, or neurological conditions?",
          "answer": "No significant systemic disease. Serum creatinine 1.1 mg/dL with normal renal function, liver function tests within normal limits, prior echocardiography showing preserved ejection fraction of 55%, and no neurological symptoms or prior stroke.",
          "evidence_quote": "Serum creatinine is 1.1 mg/dL with normal renal function. Liver function tests (AST, ALT, bilirubin) are within normal limits. Echocardiography from 2 years ago showed preserved ejection fraction at 55% with no valvular disease. Patient denies neurological symptoms or prior stroke."
        }
      ],
      "verdict_changes": [
        {
          "nct_id": "NCT07346560",
          "criterion": "Proliferative vitreoretinopathy (PVR)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07346560",
          "criterion": "Recurrent retinal detachment",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07346560",
          "criterion": "Tractional retinal detachment",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07346560",
          "criterion": "Macular hole retinal detachment",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07346560",
          "criterion": "Previous pars plana vitrectomy (PPV)",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "Present within 10 days of macula-off retinal detachment based on patient-reported history of loss of central vision",
          "before": "UNCERTAIN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "Have had previous cataract surgery in the study eye",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "History of previous ocular surgery in the study eye other than uncomplicated cataract surgery with posterior chamber intraocular lens and intact posterior capsule or refractive surgery occurring at least 3 months prior to baseline visit",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "Known hepatic disease or history of significant chronic liver disease, or known renal disease",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "History of uncontrolled hypertension",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT06587945",
          "criterion": "History of stroke, transient ischemic attack, or major cardiac surgery within 3 months prior to study, or current treatment for systemic infection",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07228091",
          "criterion": "Past history of phacovitrectomy in the planned operative eye",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07228091",
          "criterion": "Past history of cataract in the planned operative eye",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07228091",
          "criterion": "Past history of vitrectomy in the planned operative eye",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "Subjects suffering RRD with inferior retinal breaks between 4- and 8-o'clock within the detached area regardless of PVR grade",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "Subjects suffering RRD requiring retinotomy inferiorly between 4- and 8-o'clock due to severe inferior PVR or inferior retinal shortening",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "Subjects with RRD with only anterior retina breaks or dialysis meeting indications for scleral buckling surgery",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "Subjects with RRD whose retinal breaks are located between the 4- and 8-o'clock positions and are not involved in the detached area",
          "before": "UNKNOWN",
          "after": "MET"
        },
        {
          "nct_id": "NCT07081945",
          "criterion": "History of epilepsy or serious psychiatric diseases",
          "before": "UNKNOWN",
          "after": "NOT_MET"
        }
      ],
      "final_ranking": [
        {
          "nct_id": "NCT07346560",
          "rank": 1,
          "eligibility": "UNCERTAIN",
          "rationale": "Presentation consistent with rhegmatogenous retinal detachment; suitability for primary ILM peeling and absence of macular scarring unconfirmed."
        },
        {
          "nct_id": "NCT06587945",
          "rank": 2,
          "eligibility": "UNCERTAIN",
          "rationale": "Clinical picture suggests macula-off RRD amenable to vitrectomy and gas tamponade; visual acuity and surgical candidacy require confirmation."
        },
        {
          "nct_id": "NCT07081945",
          "rank": 3,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: patient age 73 exceeds trial upper limit of 70 years; break location and PVR criteria not documented."
        },
        {
          "nct_id": "NCT07228091",
          "rank": 4,
          "eligibility": "INELIGIBLE",
          "rationale": "Excluded: prior cataract history in operative eye disqualifies from combined phacovitrectomy trial."
        }
      ]
    },
    "generated_at": "2026-07-08"
  }
];
