/* KSC.JUSNREM — Constitutional Intelligence Engine
   Landmark Pakistan Supreme Court Constitutional Cases Database */
(function(){
  "use strict";

  window.LANDMARK_CASES = [
    {
      id: "tamizuddin1955",
      name: "Federation of Pakistan v. Maulvi Tamizuddin Khan",
      citation: "PLD 1955 FC 240",
      year: 1955,
      bench: "Federal Court (5-member Bench led by Chief Justice Muhammad Munir)",
      impact: "Birth of the 'Doctrine of Necessity' in Pakistan",
      summary: "Following Governor-General Ghulam Muhammad's dissolution of the First Constituent Assembly, Maulvi Tamizuddin (President of the Assembly) challenged it under Section 223A of the Government of India Act 1935. The Federal Court held that Section 223A was invalid because it had not received the Governor-General's assent, thereby upholding the dissolution and establishing executive supremacy.",
      articles: ["precursor"],
      amendments: []
    },
    {
      id: "dosso1958",
      name: "The State v. Dosso",
      citation: "PLD 1958 SC (Pak.) 533",
      year: 1958,
      bench: "Supreme Court (led by Chief Justice Muhammad Munir)",
      impact: "Legalization of Military Coup d'État",
      summary: "President Iskander Mirza abrogated the 1956 Constitution and declared Martial Law. The Supreme Court, using Hans Kelsen's theory of revolutionary legality, ruled that a successful coup constitutes a law-creating fact. Under this doctrine, the old order was replaced by the new legal order of Martial Law, suspending fundamental rights.",
      articles: ["precursor"],
      amendments: []
    },
    {
      id: "asmajilani1972",
      name: "Asma Jilani v. Government of the Punjab",
      citation: "PLD 1972 SC 139",
      year: 1972,
      bench: "Supreme Court (led by Chief Justice Hamoodur Rahman)",
      impact: "Overruling of Dosso; Declaration of Usurpation",
      summary: "Challenging detentions under Yahya Khan's Martial Law, the Supreme Court declared Yahya Khan a 'usurper' and Hans Kelsen's theory inapplicable to validate usurpation of state power. The court ruled that the military cannot abrogate the Constitution, re-establishing constitutional supremacy just prior to the framing of the 1973 Constitution.",
      articles: ["precursor"],
      amendments: []
    },
    {
      id: "bhutto1977",
      name: "Begum Nusrat Bhutto v. Chief of Army Staff",
      citation: "PLD 1977 SC 657",
      year: 1977,
      bench: "Supreme Court (9-member Bench led by Chief Justice Anwarul Haq)",
      impact: "Validation of Zia-ul-Haq's Coup under Necessity",
      summary: "Following General Zia-ul-Haq's coup against PM Zulfikar Ali Bhutto, Nusrat Bhutto challenged the martial law under Article 184(3). The Supreme Court validated the military takeover under the Doctrine of Necessity, declaring it a temporary deviation required to restore public order, and granted Zia power to amend the Constitution.",
      articles: ["article-006"],
      amendments: []
    },
    {
      id: "saifullah1989",
      name: "Federation of Pakistan v. Muhammad Saifullah Khan",
      citation: "PLD 1989 SC 166",
      year: 1989,
      bench: "Supreme Court (led by Chief Justice Nasim Hasan Shah)",
      impact: "Judicial Limits on Executive Assembly Dissolution",
      summary: "President Zia-ul-Haq dissolved the National Assembly in 1988 using Article 58(2)(b). The Supreme Court held that the dissolution was unconstitutional because Zia did not have objective grounds showing that the government of the Federation could not be carried on. However, the court did not restore the assemblies to avoid disrupting upcoming elections.",
      articles: ["article-058"],
      amendments: [7] // 8th amendment introduced 58-2b
    },
    {
      id: "aljehad1996",
      name: "Al-Jehad Trust v. Federation of Pakistan",
      citation: "PLD 1996 SC 324 (The 'Judges Case')",
      year: 1996,
      bench: "Supreme Court (led by Chief Justice Sajjad Ali Shah)",
      impact: "Reinforced Judicial Independence in Judicial Appointments",
      summary: "The SC ruled that the constitutional process of 'consultation' by the President with the Chief Justice of Pakistan (for appointments to high courts and the SC) must be meaningful and binding. The executive cannot ignore the recommendations of the CJP except for sound, recorded reasons, preventing political packing of the courts.",
      articles: ["article-177", "article-193"],
      amendments: []
    },
    {
      id: "musharraf2000",
      name: "Zafar Ali Shah v. Pervez Musharraf",
      citation: "PLD 2000 SC 869",
      year: 2000,
      bench: "Supreme Court (12-member Bench led by Chief Justice Irshad Hasan Khan)",
      impact: "Validation of Pervez Musharraf's Coup",
      summary: "Following General Musharraf's military takeover in 1999, the SC validated the coup using the Doctrine of State Necessity, citing severe state instability. The court granted Musharraf a 3-year timeline to hold general elections and validated his power to amend the constitution within that period, leading to the Legal Framework Order 2002.",
      articles: ["article-006", "article-058"],
      amendments: []
    },
    {
      id: "shcba2009",
      name: "Sindh High Court Bar Association v. Federation of Pakistan",
      citation: "PLD 2009 SC 879",
      year: 2009,
      bench: "Supreme Court (14-member Bench led by Chief Justice Iftikhar Muhammad Chaudhry)",
      impact: "Definitive Burial of the Doctrine of Necessity",
      summary: "Following the lawyers' movement, the Supreme Court declared General Musharraf's November 3, 2007 emergency, the Provisional Constitution Order (PCO), and the removal of superior court judges illegal and void. The court explicitly overruled Zafar Ali Shah and held that Zia's and Musharraf's past coup justifications were invalid under the Constitution.",
      articles: ["article-006", "article-270aaa"],
      amendments: [15] // 18th amendment codified SHCBA findings
    },
    {
      id: "distbar2015",
      name: "District Bar Association Rawalpindi v. Federation of Pakistan",
      citation: "PLD 2015 SC 401",
      year: 2015,
      bench: "Supreme Court (17-member Full Court led by Chief Justice Nasir-ul-Mulk)",
      impact: "Upholding of 21st Amendment & Military Courts; Assertion of Judicial Review",
      summary: "Challenging the 21st Amendment which established military courts for terror suspects, the Full Court held that Parliament has broad powers to amend the Constitution. However, the court established that decisions of military courts are subject to judicial review by High Courts and the Supreme Court on grounds of coram non judice, lack of jurisdiction, or mala fide.",
      articles: ["article-175", "article-212"],
      amendments: [19, 20] // 21st and 22nd amendments
    },
    {
      id: "panama2017",
      name: "Imran Khan Niazi v. Mian Muhammad Nawaz Sharif",
      citation: "PLD 2017 SC 265 / PLD 2017 SC 692",
      year: 2017,
      bench: "Supreme Court (5-member Bench)",
      impact: "Permanent Disqualification of Prime Minister under Article 62",
      summary: "Following disclosures in the Panama Papers leaks, opposition politician Imran Khan sought the disqualification of PM Nawaz Sharif. The Supreme Court disqualified Sharif from public office for not being honest and truthful ('Sadiq and Ameen') under Article 62(1)(f), holding that the disqualification was permanent and extended to failure to disclose unwithdrawn receivables.",
      articles: ["article-062"],
      amendments: []
    },
    {
      id: "art63a2022",
      name: "Interpretation of Article 63A (Presidential Reference 1 of 2022)",
      citation: "PLD 2022 SC 788",
      year: 2022,
      bench: "Supreme Court (5-member Bench led by Chief Justice Umar Ata Bandial)",
      impact: "Defecting Lawmakers' Votes Invalidated under Defection Clause",
      summary: "In a presidential reference seeking interpretation of Article 63A (the defection clause), the Supreme Court ruled by a 3-2 majority that votes cast by defecting parliamentarians against their party directives in votes of confidence, budget, or constitutional amendments cannot be counted, aiming to curb political horse-trading.",
      articles: ["article-063a"],
      amendments: []
    }
  ];

})();
