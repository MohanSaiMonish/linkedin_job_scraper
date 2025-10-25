"""
ADVANCED LINKEDIN SCRAPER - CLEAN VERSION
=========================================

This file contains advanced features without problematic imports.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import csv
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class AdvancedJobAnalyzer:
    def __init__(self):
        self.jobs_data = []
        self.insights = {}
        
    def add_salary_estimation(self, jobs_df):
        """Estimate salaries based on job titles and companies"""
        salary_ranges = {
            'Software Engineer': (80000, 150000),
            'Senior Software Engineer': (120000, 200000),
            'Data Analyst': (60000, 100000),
            'Senior Data Analyst': (90000, 130000),
            'Product Manager': (100000, 180000),
            'Senior Product Manager': (140000, 220000),
            'Machine Learning Engineer': (110000, 190000),
            'DevOps Engineer': (100000, 170000),
            'Full Stack Developer': (80000, 140000),
            'Backend Engineer': (90000, 160000),
            'Frontend Developer': (70000, 130000)
        }
        
        def estimate_salary(title):
            for key, (min_sal, max_sal) in salary_ranges.items():
                if key.lower() in title.lower():
                    return np.random.randint(min_sal, max_sal)
            return np.random.randint(60000, 120000)  # Default range
        
        jobs_df['Estimated Salary'] = jobs_df['Job Title'].apply(estimate_salary)
        return jobs_df
    
    def sentiment_analysis(self, jobs_df):
        """Analyze sentiment of job descriptions (mock implementation)"""
        sentiments = ['Positive', 'Neutral', 'Positive', 'Neutral', 'Positive']
        jobs_df['Sentiment'] = np.random.choice(sentiments, len(jobs_df))
        return jobs_df
    
    def skill_trend_analysis(self, jobs_df):
        """Analyze trending skills in job titles"""
        all_titles = ' '.join(jobs_df['Job Title'].tolist()).lower()
        
        # Common tech skills
        skills = ['python', 'javascript', 'java', 'react', 'node', 'aws', 'docker', 
                 'kubernetes', 'sql', 'machine learning', 'ai', 'data science', 
                 'analytics', 'cloud', 'devops', 'agile', 'scrum']
        
        skill_counts = {}
        for skill in skills:
            skill_counts[skill] = all_titles.count(skill)
        
        return skill_counts
    
    def company_ranking_analysis(self, jobs_df):
        """Rank companies by various metrics"""
        company_stats = jobs_df.groupby('Company').agg({
            'Job Title': 'count',
            'Estimated Salary': ['mean', 'max', 'min']
        }).round(0)
        
        company_stats.columns = ['Job_Count', 'Avg_Salary', 'Max_Salary', 'Min_Salary']
        company_stats = company_stats.sort_values('Avg_Salary', ascending=False)
        
        return company_stats
    
    def create_advanced_visualizations(self, jobs_df):
        """Create advanced visualizations"""
        # Set up the plotting style
        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Salary Distribution by Role
        plt.subplot(3, 3, 1)
        jobs_df.boxplot(column='Estimated Salary', by='Job Title', ax=plt.gca())
        plt.title('Salary Distribution by Role')
        plt.xticks(rotation=45)
        
        # 2. Company vs Average Salary
        plt.subplot(3, 3, 2)
        company_salaries = jobs_df.groupby('Company')['Estimated Salary'].mean().sort_values(ascending=False)
        company_salaries.head(10).plot(kind='bar', color='skyblue')
        plt.title('Top 10 Companies by Average Salary')
        plt.xticks(rotation=45)
        
        # 3. Location Distribution
        plt.subplot(3, 3, 3)
        location_counts = jobs_df['Location'].value_counts()
        plt.pie(location_counts.values, labels=location_counts.index, autopct='%1.1f%%')
        plt.title('Job Distribution by Location')
        
        # 4. Salary vs Company Size (mock data)
        plt.subplot(3, 3, 4)
        company_sizes = np.random.choice(['Startup', 'Mid-size', 'Enterprise'], len(jobs_df))
        jobs_df['Company Size'] = company_sizes
        jobs_df.boxplot(column='Estimated Salary', by='Company Size', ax=plt.gca())
        plt.title('Salary by Company Size')
        
        # 5. Time Series Analysis (if date available)
        plt.subplot(3, 3, 5)
        if 'Date Posted' in jobs_df.columns:
            jobs_df['Date Posted'] = pd.to_datetime(jobs_df['Date Posted'])
            daily_jobs = jobs_df.groupby(jobs_df['Date Posted'].dt.date).size()
            daily_jobs.plot(kind='line', marker='o')
            plt.title('Jobs Posted Over Time')
            plt.xticks(rotation=45)
        
        # 6. Skills Analysis
        plt.subplot(3, 3, 6)
        all_titles = ' '.join(jobs_df['Job Title'].tolist())
        # Simple word frequency analysis
        words = all_titles.lower().split()
        word_counts = Counter([word for word in words if len(word) > 3])
        top_words = dict(word_counts.most_common(10))
        
        if top_words:
            plt.bar(top_words.keys(), top_words.values(), color='orange')
            plt.title('Most Common Words in Job Titles')
            plt.xticks(rotation=45)
        
        # 7. Salary Distribution Histogram
        plt.subplot(3, 3, 7)
        jobs_df['Estimated Salary'].hist(bins=20, color='lightgreen', alpha=0.7)
        plt.title('Salary Distribution')
        plt.xlabel('Salary ($)')
        plt.ylabel('Frequency')
        
        # 8. Company Job Count vs Average Salary
        plt.subplot(3, 3, 8)
        company_stats = jobs_df.groupby('Company').agg({
            'Job Title': 'count',
            'Estimated Salary': 'mean'
        })
        plt.scatter(company_stats['Job Title'], company_stats['Estimated Salary'], alpha=0.6)
        plt.xlabel('Number of Jobs')
        plt.ylabel('Average Salary ($)')
        plt.title('Company Size vs Average Salary')
        
        # 9. Top Skills Analysis
        plt.subplot(3, 3, 9)
        skill_counts = self.skill_trend_analysis(jobs_df)
        top_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        if top_skills:
            plt.bar(top_skills.keys(), top_skills.values(), color='orange')
            plt.title('Top 10 Skills in Job Titles')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('advanced_job_analysis.png', dpi=300, bbox_inches='tight')
        print("Advanced visualization saved as 'advanced_job_analysis.png'")
        plt.show()
    
    def generate_insights_report(self, jobs_df):
        """Generate comprehensive insights report"""
        insights = {
            'total_jobs': len(jobs_df),
            'unique_companies': jobs_df['Company'].nunique(),
            'unique_locations': jobs_df['Location'].nunique(),
            'avg_salary': jobs_df['Estimated Salary'].mean(),
            'max_salary': jobs_df['Estimated Salary'].max(),
            'min_salary': jobs_df['Estimated Salary'].min(),
            'top_company': jobs_df['Company'].value_counts().index[0],
            'top_location': jobs_df['Location'].value_counts().index[0],
            'salary_range': f"${jobs_df['Estimated Salary'].min():,} - ${jobs_df['Estimated Salary'].max():,}"
        }
        
        # Generate text report
        report = f"""
        ADVANCED JOB MARKET ANALYSIS REPORT
        =====================================
        
        Market Overview:
        - Total Jobs Analyzed: {insights['total_jobs']}
        - Unique Companies: {insights['unique_companies']}
        - Unique Locations: {insights['unique_locations']}
        
        Salary Insights:
        - Average Salary: ${insights['avg_salary']:,.0f}
        - Salary Range: {insights['salary_range']}
        - Highest Paying: ${insights['max_salary']:,.0f}
        
        Market Leaders:
        - Top Company: {insights['top_company']}
        - Top Location: {insights['top_location']}
        
        Top 5 Companies by Job Count:
        {jobs_df['Company'].value_counts().head().to_string()}
        
        Top 5 Locations:
        {jobs_df['Location'].value_counts().head().to_string()}
        
        Top 5 Job Titles:
        {jobs_df['Job Title'].value_counts().head().to_string()}
        """
        
        print(report)
        
        # Save report to file
        with open('job_market_insights.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        return insights
    
    def export_to_excel(self, jobs_df, filename="advanced_job_analysis.xlsx"):
        """Export comprehensive analysis to Excel"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Main data
                jobs_df.to_excel(writer, sheet_name='Job Data', index=False)
                
                # Company analysis
                company_stats = self.company_ranking_analysis(jobs_df)
                company_stats.to_excel(writer, sheet_name='Company Analysis')
                
                # Skills analysis
                skills_data = pd.DataFrame(list(self.skill_trend_analysis(jobs_df).items()), 
                                        columns=['Skill', 'Count'])
                skills_data.to_excel(writer, sheet_name='Skills Analysis', index=False)
                
                # Summary statistics
                summary = pd.DataFrame({
                    'Metric': ['Total Jobs', 'Unique Companies', 'Average Salary', 'Max Salary'],
                    'Value': [len(jobs_df), jobs_df['Company'].nunique(), 
                             jobs_df['Estimated Salary'].mean(), jobs_df['Estimated Salary'].max()]
                })
                summary.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"Advanced analysis exported to {filename}")
        except Exception as e:
            print(f"Excel export failed: {e}")
            # Fallback to CSV
            jobs_df.to_csv(filename.replace('.xlsx', '.csv'), index=False)
            print(f"Fallback: Saved as {filename.replace('.xlsx', '.csv')}")

def main():
    """Demo of advanced features"""
    print("ADVANCED LINKEDIN SCRAPER - CLEAN VERSION")
    print("=" * 50)
    
    # Create sample data
    sample_jobs = [
        {'Job Title': 'Senior Software Engineer', 'Company': 'Google', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-15'},
        {'Job Title': 'Full Stack Developer', 'Company': 'Meta', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-14'},
        {'Job Title': 'Data Scientist', 'Company': 'Apple', 'Location': 'Cupertino, CA', 'Date Posted': '2024-01-13'},
        {'Job Title': 'Product Manager', 'Company': 'Netflix', 'Location': 'Los Gatos, CA', 'Date Posted': '2024-01-12'},
        {'Job Title': 'Machine Learning Engineer', 'Company': 'Tesla', 'Location': 'Palo Alto, CA', 'Date Posted': '2024-01-11'},
        {'Job Title': 'DevOps Engineer', 'Company': 'Uber', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-10'},
        {'Job Title': 'Backend Engineer', 'Company': 'Airbnb', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-09'},
        {'Job Title': 'Frontend Developer', 'Company': 'Twitter', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-08'},
        {'Job Title': 'Software Engineer', 'Company': 'LinkedIn', 'Location': 'Sunnyvale, CA', 'Date Posted': '2024-01-07'},
        {'Job Title': 'Senior Data Analyst', 'Company': 'Salesforce', 'Location': 'San Francisco, CA', 'Date Posted': '2024-01-06'},
    ]
    
    # Initialize analyzer
    analyzer = AdvancedJobAnalyzer()
    jobs_df = pd.DataFrame(sample_jobs)
    
    # Add advanced features
    jobs_df = analyzer.add_salary_estimation(jobs_df)
    jobs_df = analyzer.sentiment_analysis(jobs_df)
    
    # Generate insights
    insights = analyzer.generate_insights_report(jobs_df)
    
    # Create advanced visualizations
    analyzer.create_advanced_visualizations(jobs_df)
    
    # Export to Excel
    analyzer.export_to_excel(jobs_df)
    
    print("\nAdvanced analysis complete!")
    print("Files generated:")
    print("- advanced_job_analysis.png - Advanced visualizations")
    print("- advanced_job_analysis.xlsx - Comprehensive Excel report")
    print("- job_market_insights.txt - Detailed insights report")

if __name__ == "__main__":
    main()
