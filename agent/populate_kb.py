import os
import django

# Django সেটিংস সেট করুন
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_agent.settings')
django.setup()

from agent.models import KnowledgeBase

# আপনার দেওয়া Q&A গুলো এখানে যোগ করুন
qa_data = [
    # SECTION 1: General Introduction
    {
        'question': 'এটা কী ধরনের সফটওয়্যার?',
        'answer': 'এটা একটি complete School Management Software যেখানে ছাত্র ভর্তি থেকে শুরু করে attendance, exam, result, fees, SMS notification, accounts, teacher management—সবকিছু এক জায়গা থেকে পরিচালনা করা যায়।',
        'language': 'bn',
        'category': 'General'
    },
    {
        'question': 'এটা কি শুধু English medium এর জন্য?',
        'answer': 'না স্যার/ম্যাডাম, এটা Bangla & English—দুই মাধ্যমের স্কুলের জন্য ব্যবহারযোগ্য। চাইলে Madrasah বা Coaching management হিসেবেও customize করা যায়।',
        'language': 'bn',
        'category': 'General'
    },
    {
        'question': 'আপনারা কয়টা স্কুলে ব্যবহার করছেন?',
        'answer': 'আমাদের সফটওয়্যার বর্তমানে একাধিক স্কুল ব্যবহার করছে এবং আমরা ধীরে ধীরে nationwide expand করছি। চাইলে আমরা demo দিয়ে real system দেখাতে পারি।',
        'language': 'bn',
        'category': 'General'
    },
    
    # SECTION 2: Pricing
    {
        'question': 'খরচ কত?',
        'answer': 'খরচ নির্ভর করে ছাত্রসংখ্যা ও feature এর উপর। সাধারণত আমরা yearly subscription ভিত্তিতে দেই যাতে স্কুল একবারে বড় investment না করে।',
        'language': 'bn',
        'category': 'Pricing'
    },
    {
        'question': 'Lifetime দিলে কত?',
        'answer': 'আমরা lifetime option দেই না, কারণ নিয়মিত update, security patch, server maintenance করতে হয়। তবে long-term package এ discount দেওয়া হয়।',
        'language': 'bn',
        'category': 'Pricing'
    },
    {
        'question': 'আলাদা আলাদা module কিনতে পারবো?',
        'answer': 'হ্যাঁ, চাইলে basic package থেকে শুরু করে gradually upgrade করা যায়।',
        'language': 'bn',
        'category': 'Pricing'
    },
    
    # SECTION 3: Security
    {
        'question': 'Data কতটা secure?',
        'answer': 'আমাদের system role-based access control ব্যবহার করে। প্রত্যেক user আলাদা login পায়। Regular backup ও encrypted connection ব্যবহার করা হয়।',
        'language': 'bn',
        'category': 'Security'
    },
    {
        'question': 'Data কি download করে নিয়ে যাবে কেউ?',
        'answer': 'না স্যার। Server-level security, restricted access এবং proper authentication ছাড়া data access করা যায় না।',
        'language': 'bn',
        'category': 'Security'
    },
    
    # SECTION 4: Features
    {
        'question': 'Result কিভাবে দিবো?',
        'answer': 'Exam create → Mark input → Auto GPA calculation → Result publish এক ক্লিকেই marksheet ও tabulation sheet generate করা যায়।',
        'language': 'bn',
        'category': 'Features'
    },
    {
        'question': 'SMS যাবে?',
        'answer': 'হ্যাঁ, attendance, fees due, result publish—সবকিছুতে auto SMS পাঠানো যায়।',
        'language': 'bn',
        'category': 'Features'
    },
    {
        'question': 'Attendance কি mobile দিয়ে নেয়া যাবে?',
        'answer': 'হ্যাঁ, mobile friendly dashboard আছে। চাইলে RFID / biometric integration করা যায়।',
        'language': 'bn',
        'category': 'Features'
    },
    {
        'question': 'Accounting আছে?',
        'answer': 'হ্যাঁ, income-expense tracking, fee collection, report, daily cash summary—সব আছে।',
        'language': 'bn',
        'category': 'Features'
    },
    
    # SECTION 5: Teacher/Staff
    {
        'question': 'শিক্ষকরা কি আলাদা login পাবে?',
        'answer': 'হ্যাঁ, teacher login থাকবে। তারা attendance, mark entry, class routine দেখতে পারবে।',
        'language': 'bn',
        'category': 'Teacher'
    },
    {
        'question': 'Guardian কি login পাবে?',
        'answer': 'হ্যাঁ, guardian login থাকবে যেখানে তারা attendance, result, notice দেখতে পারবে।',
        'language': 'bn',
        'category': 'Teacher'
    },
    
    # SECTION 6: Technical
    {
        'question': 'এটা কি offline চলবে?',
        'answer': 'এটা cloud-based system। Internet থাকলেই যেকোনো জায়গা থেকে access করা যাবে।',
        'language': 'bn',
        'category': 'Technical'
    },
    {
        'question': 'Server কে maintain করবে?',
        'answer': 'আমরা সম্পূর্ণ server maintenance করি। স্কুলকে আলাদা IT team রাখতে হবে না।',
        'language': 'bn',
        'category': 'Technical'
    },
    {
        'question': 'Custom feature লাগলে?',
        'answer': 'হ্যাঁ, custom development করা যায়। Feature অনুযায়ী আলাদা costing হবে।',
        'language': 'bn',
        'category': 'Technical'
    },
    
    # SECTION 7: Comparison
    {
        'question': 'অন্য সফটওয়্যার থেকে আলাদা কী?',
        'answer': '✔ User friendly ✔ Bangla supported ✔ Customizable ✔ Dedicated support ✔ Regular update',
        'language': 'bn',
        'category': 'Comparison'
    },
    
    # SECTION 8: Support
    {
        'question': 'Problem হলে?',
        'answer': 'আমাদের support team phone, WhatsApp, remote support দিয়ে help করবে।',
        'language': 'bn',
        'category': 'Support'
    },
    {
        'question': 'Training দিবেন?',
        'answer': 'হ্যাঁ, admin ও teacher দের training দেওয়া হয় (online / onsite)।',
        'language': 'bn',
        'category': 'Support'
    },
    
    # SECTION 9: Objection Handling
    {
        'question': 'আমরা এখন manual system চালাচ্ছি, software লাগবে কেন?',
        'answer': 'Manual system এ— ❌ হিসাব ভুল হয় ❌ Data হারিয়ে যায় ❌ রিপোর্ট বানাতে সময় লাগে Software ব্যবহার করলে— ✅ ১ ক্লিকে রিপোর্ট ✅ Parent communication automated ✅ Transparency ✅ সময় বাঁচে',
        'language': 'bn',
        'category': 'Objection Handling'
    },
    
    # বাংলিশ Version (Romanized Bengali)
    {
        'question': 'eta ki dhoroner software?',
        'answer': 'এটা একটি complete School Management Software যেখানে ছাত্র ভর্তি থেকে শুরু করে attendance, exam, result, fees, SMS notification, accounts, teacher management—সবকিছু এক জায়গা থেকে পরিচালনা করা যায়।',
        'language': 'banglish',
        'category': 'General'
    },
    {
        'question': 'software er dam koto?',
        'answer': 'খরচ নির্ভর করে ছাত্রসংখ্যা ও feature এর উপর। সাধারণত আমরা yearly subscription ভিত্তিতে দেই যাতে স্কুল একবারে বড় investment না করে।',
        'language': 'banglish',
        'category': 'Pricing'
    },
    {
        'question': 'SMS jabe?',
        'answer': 'হ্যাঁ, attendance, fees due, result publish—সবকিছুতে auto SMS পাঠানো যায়।',
        'language': 'banglish',
        'category': 'Features'
    },
    
    # English Version
    {
        'question': 'What type of software is this?',
        'answer': 'This is a complete School Management Software where you can manage everything from student admission to attendance, exam, result, fees, SMS notification, accounts, and teacher management from one place.',
        'language': 'en',
        'category': 'General'
    },
    {
        'question': 'How much does it cost?',
        'answer': 'The cost depends on the number of students and features. We offer yearly subscriptions so schools don\'t have to make a large one-time investment.',
        'language': 'en',
        'category': 'Pricing'
    },
    {
        'question': 'Do you send SMS?',
        'answer': 'Yes, automatic SMS can be sent for attendance, fees due, result publishing, and more.',
        'language': 'en',
        'category': 'Features'
    },
]

def populate_database():
    """ডাটাবেসে Q&A গুলো যোগ করুন"""
    count = 0
    for item in qa_data:
        # চেক করুন আগে থেকে আছে কিনা (duplicate এড়াতে)
        existing = KnowledgeBase.objects.filter(
            question=item['question'], 
            language=item['language']
        ).first()
        
        if not existing:
            KnowledgeBase.objects.create(
                question=item['question'],
                answer=item['answer'],
                language=item['language'],
                category=item['category']
            )
            count += 1
            print(f"✅ Added: {item['question'][:50]}...")
        else:
            print(f"⏭️ Already exists: {item['question'][:50]}...")
    
    print(f"\n🎉 Total {count} new entries added successfully!")

if __name__ == '__main__':
    populate_database()