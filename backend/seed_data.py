import random
from datetime import datetime, timedelta
from bson import ObjectId

def generate_dummy_data(db):
    """Generate all dummy data and insert into MongoDB"""

    now = datetime.utcnow()

    # ─── EXAMS ───────────────────────────────────────────────────────
    exams = [
        {"_id": ObjectId(), "name": "JEE Main", "description": "Joint Entrance Examination for Engineering", "icon": "⚡", "color": "#25D366"},
        {"_id": ObjectId(), "name": "NEET", "description": "National Eligibility cum Entrance Test for Medical", "icon": "🧬", "color": "#128C7E"},
        {"_id": ObjectId(), "name": "UPSC CSE", "description": "Civil Services Examination", "icon": "🏛️", "color": "#075E54"},
        {"_id": ObjectId(), "name": "CAT", "description": "Common Admission Test for MBA", "icon": "📊", "color": "#34B7F1"},
        {"_id": ObjectId(), "name": "GATE", "description": "Graduate Aptitude Test in Engineering", "icon": "🔧", "color": "#ECE5DD"},
    ]

    # ─── SUBJECTS ────────────────────────────────────────────────────
    subjects_map = {
        "JEE Main": [
            {"name": "Physics", "icon": "⚛️"},
            {"name": "Chemistry", "icon": "🧪"},
            {"name": "Mathematics", "icon": "📐"},
        ],
        "NEET": [
            {"name": "Biology", "icon": "🌿"},
            {"name": "Physics", "icon": "⚛️"},
            {"name": "Chemistry", "icon": "🧪"},
        ],
        "UPSC CSE": [
            {"name": "General Studies", "icon": "📚"},
            {"name": "Current Affairs", "icon": "📰"},
            {"name": "Indian Polity", "icon": "🏛️"},
        ],
        "CAT": [
            {"name": "Quantitative Aptitude", "icon": "🔢"},
            {"name": "Verbal Ability", "icon": "📝"},
            {"name": "Data Interpretation", "icon": "📊"},
        ],
        "GATE": [
            {"name": "Data Structures", "icon": "🌲"},
            {"name": "Algorithms", "icon": "⚙️"},
            {"name": "Computer Networks", "icon": "🌐"},
        ],
    }

    all_subjects = []
    for exam in exams:
        for s in subjects_map.get(exam["name"], []):
            all_subjects.append({
                "_id": ObjectId(),
                "exam_id": str(exam["_id"]),
                "name": s["name"],
                "icon": s["icon"],
            })

    # ─── CHAPTERS ────────────────────────────────────────────────────
    chapters_template = [
        "Fundamentals", "Advanced Concepts", "Problem Solving",
        "Applications", "Practice Set A", "Practice Set B"
    ]
    all_chapters = []
    for subject in all_subjects:
        for ch_name in chapters_template:
            all_chapters.append({
                "_id": ObjectId(),
                "subject_id": str(subject["_id"]),
                "exam_id": subject["exam_id"],
                "name": f"{ch_name}",
                "description": f"{ch_name} for {subject['name']}",
                "question_count": random.randint(10, 20),
            })

    # ─── QUESTIONS ───────────────────────────────────────────────────
    question_bank = {
        "Physics": [
            ("What is Newton's First Law of Motion?", ["An object stays at rest unless acted upon", "F = ma", "Action = Reaction", "Energy is conserved"], 0),
            ("What is the SI unit of force?", ["Joule", "Newton", "Pascal", "Watt"], 1),
            ("What is the speed of light in vacuum?", ["3×10⁸ m/s", "3×10⁶ m/s", "3×10¹⁰ m/s", "3×10⁴ m/s"], 0),
            ("Which law relates pressure and volume of gas?", ["Charles's Law", "Boyle's Law", "Avogadro's Law", "Gay-Lussac's Law"], 1),
            ("Ohm's Law states that V equals?", ["I × R", "I / R", "R / I", "I + R"], 0),
            ("What is the unit of electric charge?", ["Volt", "Ampere", "Coulomb", "Ohm"], 2),
            ("Which particle has no electric charge?", ["Proton", "Electron", "Neutron", "Positron"], 2),
            ("The phenomenon of bending of light is called?", ["Reflection", "Refraction", "Diffraction", "Dispersion"], 1),
            ("What is the formula for kinetic energy?", ["mgh", "½mv²", "mv", "Fd"], 1),
            ("Magnetic force on a current-carrying conductor is given by?", ["F = qE", "F = BIL", "F = mv²/r", "F = kq²/r²"], 1),
        ],
        "Chemistry": [
            ("What is the atomic number of Carbon?", ["4", "6", "8", "12"], 1),
            ("Which gas is most abundant in Earth's atmosphere?", ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"], 2),
            ("pH of pure water is?", ["0", "7", "14", "1"], 1),
            ("What is the chemical formula of table salt?", ["NaCl", "KCl", "CaCl₂", "MgCl₂"], 0),
            ("Avogadro's number is approximately?", ["6.022×10²³", "6.022×10²⁰", "3.14×10²³", "1.38×10²³"], 0),
            ("Which acid is present in vinegar?", ["Citric acid", "Hydrochloric acid", "Acetic acid", "Lactic acid"], 2),
            ("The lightest element in the periodic table is?", ["Helium", "Lithium", "Hydrogen", "Beryllium"], 2),
            ("What type of bond exists in NaCl?", ["Covalent", "Metallic", "Ionic", "Hydrogen"], 2),
            ("Which gas is produced during photosynthesis?", ["CO₂", "O₂", "N₂", "H₂"], 1),
            ("Rusting of iron is a type of?", ["Physical change", "Chemical change", "Nuclear change", "Phase change"], 1),
        ],
        "Mathematics": [
            ("What is the value of π (pi) approximately?", ["3.14", "2.71", "1.41", "1.73"], 0),
            ("The derivative of sin(x) is?", ["cos(x)", "-cos(x)", "tan(x)", "-sin(x)"], 0),
            ("What is the sum of angles in a triangle?", ["90°", "180°", "270°", "360°"], 1),
            ("∫x dx equals?", ["x²", "x²/2 + C", "2x + C", "x + C"], 1),
            ("What is the quadratic formula?", ["(-b ± √(b²-4ac))/2a", "(b ± √(b²-4ac))/2a", "(-b ± √(b+4ac))/2a", "(-b ± √(b²+4ac))/2a"], 0),
            ("The value of log₁₀(100) is?", ["1", "2", "10", "100"], 1),
            ("How many sides does a hexagon have?", ["5", "6", "7", "8"], 1),
            ("What is the formula for area of a circle?", ["2πr", "πr²", "πd", "2πr²"], 1),
            ("The Pythagorean theorem states?", ["a² + b² = c²", "a + b = c", "a² - b² = c²", "a² × b² = c²"], 0),
            ("The factorial of 5 (5!) is?", ["100", "120", "60", "24"], 1),
        ],
        "Biology": [
            ("The powerhouse of the cell is?", ["Nucleus", "Ribosome", "Mitochondria", "Golgi body"], 2),
            ("DNA stands for?", ["Deoxyribonucleic Acid", "Diribonucleic Acid", "Deoxyribose Nucleic Acid", "Dual Nucleic Acid"], 0),
            ("How many chambers does the human heart have?", ["2", "3", "4", "5"], 2),
            ("Which blood group is universal donor?", ["A", "B", "AB", "O"], 3),
            ("Photosynthesis occurs in which organelle?", ["Mitochondria", "Nucleus", "Chloroplast", "Vacuole"], 2),
            ("The basic unit of life is?", ["Tissue", "Organ", "Cell", "Organism"], 2),
            ("Which vitamin is produced by sunlight?", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], 3),
            ("The largest organ of the human body is?", ["Heart", "Liver", "Brain", "Skin"], 3),
            ("RNA differs from DNA in containing?", ["Thymine", "Uracil", "Guanine", "Adenine"], 1),
            ("Which gas do plants absorb during photosynthesis?", ["O₂", "N₂", "CO₂", "H₂"], 2),
        ],
        "General Studies": [
            ("Who is known as the Father of the Indian Constitution?", ["Gandhi", "Nehru", "Ambedkar", "Patel"], 2),
            ("The capital of India is?", ["Mumbai", "Delhi", "Kolkata", "Chennai"], 1),
            ("India got independence in which year?", ["1945", "1946", "1947", "1948"], 2),
            ("Which is the longest river in India?", ["Yamuna", "Brahmaputra", "Ganga", "Godavari"], 2),
            ("The Rajya Sabha has how many elected members?", ["238", "240", "245", "250"], 2),
            ("Who wrote 'Discovery of India'?", ["Gandhi", "Nehru", "Ambedkar", "Tagore"], 1),
            ("Which article of the Indian Constitution deals with Right to Equality?", ["Article 12", "Article 14", "Article 19", "Article 21"], 1),
            ("The first Prime Minister of India was?", ["Sardar Patel", "Rajendra Prasad", "Jawaharlal Nehru", "B.R. Ambedkar"], 2),
            ("How many states are in India?", ["27", "28", "29", "30"], 1),
            ("The Supreme Court of India is located in?", ["Mumbai", "Delhi", "Kolkata", "Chennai"], 1),
        ],
        "Quantitative Aptitude": [
            ("If 2x + 3 = 11, what is x?", ["3", "4", "5", "6"], 1),
            ("What is 15% of 200?", ["25", "30", "35", "40"], 1),
            ("A train travels 360 km in 4 hours. Speed?", ["80 km/h", "90 km/h", "100 km/h", "110 km/h"], 1),
            ("The LCM of 4 and 6 is?", ["10", "12", "16", "24"], 1),
            ("What is the square root of 144?", ["10", "11", "12", "14"], 2),
            ("If a = 5, b = 3, a² - b² = ?", ["16", "25", "34", "7"], 0),
            ("Ratio 3:4 equivalent to?", ["6:9", "9:12", "12:9", "4:3"], 1),
            ("Simple interest on ₹1000 at 10% for 2 years?", ["₹100", "₹150", "₹200", "₹250"], 2),
            ("Find the average of 10, 20, 30, 40, 50?", ["25", "30", "35", "40"], 1),
            ("If cost price is ₹80 and selling price is ₹100, profit % is?", ["20%", "25%", "15%", "10%"], 1),
        ],
        "Data Structures": [
            ("What is the time complexity of binary search?", ["O(n)", "O(log n)", "O(n²)", "O(1)"], 1),
            ("Which data structure uses LIFO?", ["Queue", "Stack", "Linked List", "Tree"], 1),
            ("Which data structure uses FIFO?", ["Stack", "Queue", "Heap", "Graph"], 1),
            ("The height of a complete binary tree with n nodes?", ["O(n)", "O(log n)", "O(n log n)", "O(√n)"], 1),
            ("Hash table average case for search is?", ["O(1)", "O(n)", "O(log n)", "O(n²)"], 0),
            ("Which traversal visits root first?", ["Inorder", "Postorder", "Preorder", "BFS"], 2),
            ("DFS uses which data structure?", ["Queue", "Stack", "Heap", "Array"], 1),
            ("BFS uses which data structure?", ["Stack", "Queue", "Priority Queue", "Deque"], 1),
            ("Linked list access time is?", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2),
            ("A graph with no cycles is called?", ["Tree", "Forest", "DAG", "Bipartite"], 0),
        ],
        "Current Affairs": [
            ("Which country hosted G20 Summit 2023?", ["USA", "China", "India", "Germany"], 2),
            ("Who is the current Secretary-General of UN?", ["Ban Ki-moon", "António Guterres", "Kofi Annan", "Boutros Ghali"], 1),
            ("Chandrayaan-3 landed on which part of Moon?", ["North Pole", "South Pole", "Equator", "Far Side"], 1),
            ("India's GDP rank in world (2023)?", ["3rd", "4th", "5th", "6th"], 2),
            ("Which country is hosting FIFA World Cup 2026?", ["Qatar", "Brazil", "USA/Canada/Mexico", "Germany"], 2),
            ("Digital India initiative launched in which year?", ["2013", "2014", "2015", "2016"], 2),
            ("India's first indigenous aircraft carrier is?", ["INS Vikrant", "INS Viraat", "INS Kolkata", "INS Chennai"], 0),
            ("Operation Brahma was launched to help which country?", ["Nepal", "Bangladesh", "Myanmar", "Sri Lanka"], 2),
            ("Rafale fighter jets are from which country?", ["USA", "Russia", "France", "UK"], 2),
            ("UPI was launched by?", ["RBI", "NPCI", "SBI", "Finance Ministry"], 1),
        ],
        "Verbal Ability": [
            ("Choose the synonym of 'Benevolent'?", ["Cruel", "Kind", "Selfish", "Lazy"], 1),
            ("Choose the antonym of 'Verbose'?", ["Talkative", "Concise", "Eloquent", "Fluent"], 1),
            ("Identify the correctly spelled word?", ["Accomodation", "Accommodation", "Acommodation", "Accomadation"], 1),
            ("Choose the correct form: 'She __ to the market yesterday'", ["go", "went", "goes", "going"], 1),
            ("What is a metaphor?", ["Direct comparison using like/as", "Implied comparison", "Exaggeration", "Rhyming scheme"], 1),
            ("The plural of 'Crisis' is?", ["Crisises", "Crisis", "Crises", "Crisiss"], 2),
            ("Select the passive voice: 'The dog bit the man'", ["The man was bit by the dog", "The man is bitten by dog", "The man was bitten by the dog", "The dog was biting man"], 2),
            ("Choose the correct preposition: 'She is good ___ cooking'", ["in", "at", "on", "for"], 1),
            ("Which figure of speech: 'The wind whispered'?", ["Simile", "Metaphor", "Personification", "Alliteration"], 2),
            ("The reading passage says... 'The author's tone is?'", ["Aggressive", "Sarcastic", "Neutral", "Melancholic"], 2),
        ],
        "Computer Networks": [
            ("The OSI model has how many layers?", ["5", "6", "7", "8"], 2),
            ("HTTP operates at which layer?", ["Transport", "Network", "Application", "Session"], 2),
            ("IP address has how many bits (IPv4)?", ["16", "32", "64", "128"], 1),
            ("TCP is a __ protocol?", ["Connectionless", "Connection-oriented", "Broadcast", "Multicast"], 1),
            ("DNS converts domain name to?", ["MAC address", "IP address", "Port number", "Subnet mask"], 1),
            ("Default subnet mask for Class C?", ["255.0.0.0", "255.255.0.0", "255.255.255.0", "255.255.255.255"], 2),
            ("FTP uses port number?", ["20/21", "22", "25", "80"], 0),
            ("Which protocol assigns IP addresses dynamically?", ["DNS", "FTP", "DHCP", "SMTP"], 2),
            ("Bandwidth is measured in?", ["Hz", "bps", "dB", "Watts"], 1),
            ("ARP stands for?", ["Address Resolution Protocol", "Advanced Routing Protocol", "Automatic Response Protocol", "Address Routing Protocol"], 0),
        ],
        "Indian Polity": [
            ("The Indian Constitution came into effect on?", ["26 Jan 1947", "15 Aug 1947", "26 Jan 1950", "26 Nov 1949"], 2),
            ("How many fundamental rights are in the Indian Constitution?", ["5", "6", "7", "8"], 1),
            ("Who appoints the Chief Justice of India?", ["Prime Minister", "Parliament", "President", "Vice President"], 2),
            ("Rajya Sabha is also called?", ["Lower House", "Upper House", "Federal House", "State House"], 1),
            ("Emergency provisions are in which part of the Constitution?", ["Part XVII", "Part XVIII", "Part XIX", "Part XX"], 1),
            ("The Comptroller and Auditor General is appointed by?", ["PM", "President", "Supreme Court", "Parliament"], 1),
            ("Which schedule deals with anti-defection?", ["8th", "9th", "10th", "11th"], 2),
            ("The term of Lok Sabha is?", ["4 years", "5 years", "6 years", "7 years"], 1),
            ("Which article grants citizenship?", ["Article 5", "Article 9", "Article 11", "Article 15"], 0),
            ("The Preamble of India starts with?", ["We the People of India", "We the Citizens", "We the Sovereign People", "We the Democratic People"], 0),
        ],
        "Algorithms": [
            ("Quick sort worst case complexity?", ["O(n log n)", "O(n)", "O(n²)", "O(log n)"], 2),
            ("Merge sort time complexity?", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], 1),
            ("Bubble sort best case?", ["O(n²)", "O(n log n)", "O(n)", "O(1)"], 2),
            ("Dijkstra's algorithm finds?", ["Maximum spanning tree", "Shortest path", "Minimum spanning tree", "Topological order"], 1),
            ("Dynamic programming uses?", ["Memoization/Tabulation", "Only Recursion", "Greedy approach", "Backtracking"], 0),
            ("Which algorithm for minimum spanning tree?", ["Dijkstra", "Kruskal", "Floyd-Warshall", "Bellman-Ford"], 1),
            ("Floyd-Warshall complexity?", ["O(n²)", "O(n³)", "O(n log n)", "O(2ⁿ)"], 1),
            ("Which sorting is stable?", ["Quick sort", "Heap sort", "Merge sort", "Selection sort"], 2),
            ("Binary search requires data to be?", ["Random", "Sorted", "Linked", "Hashed"], 1),
            ("Greedy algorithm is optimal for?", ["0/1 Knapsack", "Fractional Knapsack", "Longest common subsequence", "Matrix chain multiplication"], 1),
        ],
        "Data Interpretation": [
            ("If sales increased from 100 to 120, percentage increase?", ["10%", "20%", "15%", "25%"], 1),
            ("Average of 5, 10, 15, 20, 25?", ["13", "14", "15", "16"], 2),
            ("Pie chart shows 90° for category A. Its percentage?", ["20%", "25%", "30%", "35%"], 1),
            ("Bar graph value doubled means growth of?", ["50%", "100%", "200%", "150%"], 1),
            ("Compound interest formula?", ["P(1+r/n)^nt", "P+PRT", "P(1-r)^t", "Prt"], 0),
            ("If ratio is 2:3:5, the largest share from ₹100?", ["₹20", "₹30", "₹50", "₹40"], 2),
            ("Median of 3,5,7,9,11?", ["5", "7", "9", "11"], 1),
            ("Mode of 2,3,3,4,5,3?", ["2", "3", "4", "5"], 1),
            ("Standard deviation measures?", ["Central tendency", "Dispersion", "Correlation", "Regression"], 1),
            ("A table shows sales Q1=200, Q2=250. Q2 growth?", ["20%", "25%", "30%", "50%"], 1),
        ],
    }

    # Default questions for unmapped subjects
    default_questions = question_bank.get("Physics", [])

    all_questions = []
    for chapter in all_chapters:
        # Find subject name
        subject = next((s for s in all_subjects if str(s["_id"]) == chapter["subject_id"]), None)
        if not subject:
            continue
        q_pool = question_bank.get(subject["name"], default_questions)
        num_q = min(chapter["question_count"], len(q_pool))
        selected = random.sample(q_pool, min(num_q, len(q_pool)))
        for q_text, options, correct_idx in selected:
            all_questions.append({
                "_id": ObjectId(),
                "chapter_id": str(chapter["_id"]),
                "subject_id": chapter["subject_id"],
                "exam_id": chapter["exam_id"],
                "question_text": q_text,
                "options": options,
                "correct_option": correct_idx,
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "explanation": f"The correct answer is option {correct_idx + 1}.",
            })

    # ─── USERS ───────────────────────────────────────────────────────
    user_names = [
        "Aarav Sharma", "Priya Patel", "Rohit Kumar", "Sneha Reddy", "Amit Singh",
        "Kavya Nair", "Rajesh Gupta", "Meera Joshi", "Vikram Bose", "Ananya Das",
        "Suresh Iyer", "Pooja Mehta", "Kiran Rao", "Deepa Pillai", "Arjun Verma",
        "Nisha Chauhan", "Saurav Ghosh", "Lakshmi Krishnan", "Rahul Dubey", "Simran Kaur"
    ]
    users = []
    for name in user_names:
        users.append({
            "_id": ObjectId(),
            "name": name,
            "email": name.lower().replace(" ", ".") + "@example.com",
            "created_at": now - timedelta(days=random.randint(10, 365)),
            "last_seen": now - timedelta(hours=random.randint(0, 72)),
        })

    # ─── QUIZ SESSIONS ───────────────────────────────────────────────
    sessions = []
    answers_log = []

    for i in range(150):
        user = random.choice(users)
        chapter = random.choice(all_chapters)
        chapter_questions = [q for q in all_questions if q["chapter_id"] == str(chapter["_id"])]
        if not chapter_questions:
            continue

        session_started = now - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        num_answered = random.randint(1, len(chapter_questions))
        completed = num_answered == len(chapter_questions) and random.random() > 0.3

        session_id = ObjectId()
        score = 0
        session_answers = []

        for j, q in enumerate(chapter_questions[:num_answered]):
            shown_at = session_started + timedelta(seconds=j * random.randint(15, 90))
            response_time = random.randint(5, 120)
            submitted_at = shown_at + timedelta(seconds=response_time)
            selected = random.randint(0, 3)
            is_correct = selected == q["correct_option"]
            if is_correct:
                score += 1

            ans = {
                "_id": ObjectId(),
                "session_id": str(session_id),
                "question_id": str(q["_id"]),
                "user_id": str(user["_id"]),
                "selected_option": selected,
                "is_correct": is_correct,
                "question_shown_at": shown_at,
                "answer_submitted_at": submitted_at,
                "response_duration_seconds": response_time,
                "date": shown_at.date().isoformat(),
                "hour": shown_at.hour,
            }
            session_answers.append(ans)

        answers_log.extend(session_answers)

        sessions.append({
            "_id": session_id,
            "user_id": str(user["_id"]),
            "exam_id": chapter["exam_id"],
            "subject_id": chapter["subject_id"],
            "chapter_id": str(chapter["_id"]),
            "started_at": session_started,
            "completed_at": session_started + timedelta(minutes=random.randint(5, 40)) if completed else None,
            "is_completed": completed,
            "total_questions": len(chapter_questions),
            "answered_questions": num_answered,
            "score": score,
            "date": session_started.date().isoformat(),
            "hour": session_started.hour,
        })

    return {
        "exams": exams,
        "subjects": all_subjects,
        "chapters": all_chapters,
        "questions": all_questions,
        "users": users,
        "sessions": sessions,
        "answers": answers_log,
    }
