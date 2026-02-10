"""
Dashboard Generator

This module generates an HTML dashboard with visuals
"""

import json
from datetime import datetime
from data_processor import PortfolioDataProcessor


class DashboardGenerator:
    """Generate an interactive HTML dashboard for portfolio analysis."""
    
    def __init__(self, data):
        """Initialize with processed data."""
        self.data = data
        
    def generate_html(self):
        """Generate the complete HTML dashboard."""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fortitude Re - Alternatives Portfolio Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .dashboard-container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .nav-tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
            padding: 0 40px;
        }}
        
        .nav-tab {{
            padding: 20px 30px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            font-weight: 600;
            color: #6c757d;
            transition: all 0.3s ease;
        }}
        
        .nav-tab:hover {{
            color: #495057;
            background: #e9ecef;
        }}
        
        .nav-tab.active {{
            color: #2a5298;
            border-bottom-color: #2a5298;
            background: white;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
            animation: fadeIn 0.5s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .metric-card h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metric-card .value {{
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .metric-card .subtext {{
            font-size: 0.85em;
            opacity: 0.8;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .chart-container h2 {{
            color: #2a5298;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 400px;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .data-table thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .data-table th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        .data-table td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        .data-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .positive {{
            color: #28a745;
            font-weight: 600;
        }}
        
        .negative {{
            color: #dc3545;
            font-weight: 600;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }}
        
        .grid-2 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 30px;
        }}
        
        
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #2a5298;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }}
        
        .info-box h3 {{
            color: #2a5298;
            margin-bottom: 10px;
        }}
        
        .info-box ul {{
            margin-left: 20px;
            color: #495057;
        }}
        
        .info-box li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Header -->
        <div class="header">
            <h1>Fortitude Re - Alternatives Portfolio Dashboard</h1>
            <p>Comprehensive Analysis & Performance Tracking</p>
            <p style="font-size: 0.9em; margin-top: 10px;">
                Data Period: {self.data['metadata']['data_period']} | 
                Generated: {self.data['metadata']['generated_date']}
            </p>
        </div>
        
        <!-- Navigation Tabs -->
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('overview')">Overview</div>
            <div class="nav-tab" onclick="showTab('composition')">Composition</div>
            <div class="nav-tab" onclick="showTab('performance')">Performance</div>
            <div class="nav-tab" onclick="showTab('trends')">Trends</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <!-- Overview Tab -->
            <div id="overview" class="tab-content active">
                <div class="info-box">
                    <h3>📊 Dashboard Overview</h3>
                    <ul>
                        <li><strong>Purpose:</strong> Track and analyze Fortitude Re's Alternatives quarterly portfolio performance and composition</li>
                        <li><strong>Alternatives Defined:</strong> Private Equity, Real Assets, Hedge Funds, Credit Funds, and Real Estate</li>
                        <li><strong>Coverage:</strong> {self.data['metadata']['alternatives_records']:,} investment records</li>
                        <li><strong>Update Frequency:</strong> Quarterly (easily refreshable with new quarterly data)</li>
                    </ul>
                </div>
                
                <h2 style="color: #2a5298; margin-bottom: 20px;">Quarterly Metrics Summary</h2>
                <div class="metrics-grid">
                    {self._generate_metric_cards()}
                </div>
                
                <div class="grid-2">
                    <div class="chart-container">
                        <h2>Total End NAV Trend: Alts vs Non-Alts</h2>
                        <div class="chart-wrapper">
                            <canvas id="navComparisonChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <h2>Quarterly Return Performance</h2>
                        <div class="chart-wrapper">
                            <canvas id="quarterlyReturnChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Composition Tab -->
            <div id="composition" class="tab-content">
                <h2 style="color: #2a5298; margin-bottom: 20px;">Portfolio Composition Analysis</h2>
                
                <div class="grid-2">
                    <div class="chart-container">
                        <h2>Alternatives by Asset Class (Current)</h2>
                        <div class="chart-wrapper">
                            <canvas id="compositionPieChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="chart-container">
                        <h2>Asset Class Distribution (NAV)</h2>
                        <div class="chart-wrapper">
                            <canvas id="compositionBarChart"></canvas>
                        </div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Detailed Composition Breakdown</h2>
                    {self._generate_composition_table()}
                </div>
            </div>
            
            <!-- Performance Tab -->
            <div id="performance" class="tab-content">
                <h2 style="color: #2a5298; margin-bottom: 20px;">Performance Analysis</h2>
                
                <div class="chart-container">
                    <h2>Returns by Asset Class (Most Recent Quarter)</h2>
                    <div class="chart-wrapper">
                        <canvas id="performanceChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Quarterly Performance Metrics</h2>
                    <div class="chart-wrapper">
                        <canvas id="incomeYieldChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Performance Details by Asset Class</h2>
                    {self._generate_performance_table()}
                </div>
            </div>
            
            <!-- Trends Tab -->
            <div id="trends" class="tab-content">
                <h2 style="color: #2a5298; margin-bottom: 20px;">Historical Trends</h2>
                
                <div class="chart-container">
                    <h2>NAV Growth by Asset Class Over Time</h2>
                    <div class="chart-wrapper">
                        <canvas id="trendsLineChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Cash Flow Analysis: Contributions vs Distributions</h2>
                    <div class="chart-wrapper">
                        <canvas id="cashFlowChart"></canvas>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h2>Investment Income Trends</h2>
                    <div class="chart-wrapper">
                        <canvas id="incomeChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p><strong>Fortitude Re - Alternatives Portfolio Dashboard</strong></p>
            <p>Data sourced from FRL_Portfolio dataset.</p>
            <p>To update with new quarterly data, run: python run_dashboard.py</p>
        </div>
    </div>

    <script>
        // Embedded data
        const dashboardData = {json.dumps(self.data)};
        
        // Tab switching functionality
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Remove active from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Format currency
        function formatCurrency(value) {{
            if (value >= 1e9) return '$' + (value/1e9).toFixed(2) + 'B';
            if (value >= 1e6) return '$' + (value/1e6).toFixed(1) + 'M';
            if (value >= 1e3) return '$' + (value/1e3).toFixed(1) + 'K';
            return '$' + value.toFixed(0);
        }}
        
        // Format percentage
        function formatPercent(value) {{
            return value.toFixed(2) + '%';
        }}
        
        // Chart.js default configuration
        Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif";
        Chart.defaults.font.size = 12;
        Chart.defaults.color = '#495057';
        
        // Color palette
        const colors = {{
            primary: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'],
            gradient: [
                'rgba(102, 126, 234, 0.8)',
                'rgba(118, 75, 162, 0.8)',
                'rgba(240, 147, 251, 0.8)',
                'rgba(79, 172, 254, 0.8)',
                'rgba(67, 233, 123, 0.8)'
            ]
        }};
        
        // Initialize all charts
        function initializeCharts() {{
            createNAVComparisonChart();
            createQuarterlyReturnChart();
            createCompositionPieChart();
            createCompositionBarChart();
            createPerformanceChart();
            createIncomeYieldChart();
            createTrendsLineChart();
            createCashFlowChart();
            createIncomeChart();
        }}
        
        // NAV Comparison Chart
        function createNAVComparisonChart() {{
            // Pull time-series data for Alts 
            const altsData = dashboardData.alternatives_timeseries;
            
            const nonAltsData = dashboardData.non_alternatives_timeseries;
            
            // Create a new Chart.js line chart inside the HTML element <canvas id="navComparisonChart">
            new Chart(document.getElementById('navComparisonChart'), {{
            
                // Line chart
                type: 'line',
                
                // Data that will be plotted on the chart
                data: {{
                
                    // Labels are the dates along the x-axis (quarterly dates)
                    labels: altsData.map(d => d.Date),
                    
                    // Plot two datasets: Alts vs Non-Alts
                    datasets: [
                        {{
                            label: 'Alternatives',
                            
                            // End NAV values for Alts is Y-axis Values
                            data: altsData.map(d => d.End_NAV),
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }},
                        {{
                            label: 'Non-Alternatives',
                            data: nonAltsData.map(d => d.End_NAV),
                            borderColor: '#764ba2',
                            backgroundColor: 'rgba(118, 75, 162, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4
                        }}
                    ]
                }},
                // Options = Appearance and user-interaction settings
                options: {{
                
                    // Responsive = Resize window = true
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                font: {{ size: 14, weight: 'bold' }},
                                padding: 15
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + formatCurrency(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return formatCurrency(value);
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Quarterly Return Chart
        function createQuarterlyReturnChart() {{
            const data = dashboardData.quarterly_performance;
            
            new Chart(document.getElementById('quarterlyReturnChart'), {{
                type: 'bar',
                data: {{
                    labels: data.map(d => d.Date),
                    datasets: [{{
                        label: 'Quarterly Return %',
                        data: data.map(d => d.Return_Pct),
                        backgroundColor: data.map(d => d.Return_Pct >= 0 ? 'rgba(67, 233, 123, 0.8)' : 'rgba(255, 99, 132, 0.8)'),
                        borderColor: data.map(d => d.Return_Pct >= 0 ? '#43e97b' : '#ff6384'),
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'Return: ' + formatPercent(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: function(value) {{
                                    return value.toFixed(1) + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Composition Pie Chart
        function createCompositionPieChart() {{
            const data = dashboardData.composition;
            
            new Chart(document.getElementById('compositionPieChart'), {{
                type: 'doughnut',
                data: {{
                    labels: data.map(d => d.Asset_Class),
                    datasets: [{{
                        data: data.map(d => d.Total_NAV),
                        backgroundColor: colors.gradient,
                        borderWidth: 3,
                        borderColor: '#ffffff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{
                                padding: 15,
                                font: {{ size: 12 }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const label = context.label;
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return label + ': ' + formatCurrency(value) + ' (' + percentage + '%)';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Composition Bar Chart
        function createCompositionBarChart() {{
            const data = dashboardData.composition;
            
            new Chart(document.getElementById('compositionBarChart'), {{
                type: 'bar',
                data: {{
                    labels: data.map(d => d.Asset_Class),
                    datasets: [{{
                        label: 'Total NAV',
                        data: data.map(d => d.Total_NAV),
                        backgroundColor: colors.gradient,
                        borderColor: colors.primary,
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'NAV: ' + formatCurrency(context.parsed.x);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return formatCurrency(value);
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Performance Chart
        function createPerformanceChart() {{
            const data = dashboardData.performance_by_asset_class;
            
            new Chart(document.getElementById('performanceChart'), {{
                type: 'bar',
                data: {{
                    labels: data.map(d => d.Asset_Class),
                    datasets: [{{
                        label: 'Return %',
                        data: data.map(d => d.Return_Pct),
                        backgroundColor: colors.gradient,
                        borderColor: colors.primary,
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'Return: ' + formatPercent(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: function(value) {{
                                    return value.toFixed(1) + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Income Yield Chart
        function createIncomeYieldChart() {{
            const data = dashboardData.quarterly_performance;
            
            new Chart(document.getElementById('incomeYieldChart'), {{
                type: 'line',
                data: {{
                    labels: data.map(d => d.Date),
                    datasets: [
                        {{
                            label: 'Quarterly Return %',
                            data: data.map(d => d.Return_Pct),
                            borderColor: '#667eea',
                            backgroundColor: 'rgba(102, 126, 234, 0.1)',
                            borderWidth: 3,
                            yAxisID: 'y',
                            tension: 0.4
                        }},
                        {{
                            label: 'Income Yield %',
                            data: data.map(d => d.Income_Yield),
                            borderColor: '#43e97b',
                            backgroundColor: 'rgba(67, 233, 123, 0.1)',
                            borderWidth: 3,
                            yAxisID: 'y',
                            tension: 0.4
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                padding: 15,
                                font: {{ size: 14, weight: 'bold' }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + formatPercent(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: function(value) {{
                                    return value.toFixed(1) + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Trends Line Chart
        function createTrendsLineChart() {{
            const data = dashboardData.asset_class_trends;
            const assetClasses = [...new Set(data.map(d => d.Asset_Class))];
            
            const datasets = assetClasses.map((ac, idx) => {{
                const classData = data.filter(d => d.Asset_Class === ac);
                return {{
                    label: ac,
                    data: classData.map(d => ({{ x: d.Date, y: d.End_NAV }})),
                    borderColor: colors.primary[idx % colors.primary.length],
                    backgroundColor: colors.gradient[idx % colors.gradient.length],
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                }};
            }});
            
            new Chart(document.getElementById('trendsLineChart'), {{
                type: 'line',
                data: {{ datasets: datasets }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                padding: 10,
                                font: {{ size: 12, weight: 'bold' }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + formatCurrency(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            type: 'category',
                            title: {{ display: true, text: 'Quarter' }}
                        }},
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return formatCurrency(value);
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Cash Flow Chart
        function createCashFlowChart() {{
            const data = dashboardData.quarterly_performance;
            
            new Chart(document.getElementById('cashFlowChart'), {{
                type: 'bar',
                data: {{
                    labels: data.map(d => d.Date),
                    datasets: [
                        {{
                            label: 'Contributions',
                            data: data.map(d => d.Contributions),
                            backgroundColor: 'rgba(67, 233, 123, 0.8)',
                            borderColor: '#43e97b',
                            borderWidth: 2
                        }},
                        {{
                            label: 'Distributions',
                            data: data.map(d => -d.Distributions),
                            backgroundColor: 'rgba(255, 99, 132, 0.8)',
                            borderColor: '#ff6384',
                            borderWidth: 2
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                padding: 15,
                                font: {{ size: 14, weight: 'bold' }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + formatCurrency(Math.abs(context.parsed.y));
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{
                                callback: function(value) {{
                                    return formatCurrency(Math.abs(value));
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Income Chart
        function createIncomeChart() {{
            const data = dashboardData.quarterly_performance;
            
            new Chart(document.getElementById('incomeChart'), {{
                type: 'line',
                data: {{
                    labels: data.map(d => d.Date),
                    datasets: [{{
                        label: 'Net Investment Income',
                        data: data.map(d => d.Net_Investment_Income),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.2)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'top',
                            labels: {{
                                padding: 15,
                                font: {{ size: 14, weight: 'bold' }}
                            }}
                        }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'Income: ' + formatCurrency(context.parsed.y);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            ticks: {{
                                callback: function(value) {{
                                    return formatCurrency(value);
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Initialize charts when page loads
        window.addEventListener('load', initializeCharts);
    </script>
</body>
</html>
"""
        return html
    
    def _generate_metric_cards(self):
        """Generate HTML for metric cards."""
        metrics = self.data['key_metrics']
        
        cards = f"""
        <div class="metric-card">
            <h3>Total End NAV</h3>
            <div class="value">${metrics['total_nav']/1e9:.2f}B</div>
            <div class="subtext">Quarter Ended: {metrics['as_of_date']}</div>
        </div>
        
        <div class="metric-card">
            <h3>Weighted Return</h3>
            <div class="value">{metrics['weighted_return_pct']:.2f}%</div>
            <div class="subtext">Most Recent Quarter</div>
        </div>
        
        <div class="metric-card">
            <h3>Total Securities</h3>
            <div class="value">{metrics['num_securities']}</div>
            <div class="subtext">Across {metrics['num_asset_classes']} Asset Classes</div>
        </div>
        
        <div class="metric-card">
            <h3>Net Investment Income</h3>
            <div class="value">${metrics['total_income']/1e6:.1f}M</div>
            <div class="subtext">Most Recent Quarter</div>
        </div>
        """
        
        return cards
    
    def _generate_composition_table(self):
        """Generate HTML table for composition data."""
        composition = self.data['composition']
        
        rows = ""
        for item in composition:
            rows += f"""
            <tr>
                <td><strong>{item['Asset_Class']}</strong></td>
                <td>${item['Total_NAV']/1e9:.3f}B</td>
                <td>{item['Percentage']:.1f}%</td>
                <td>{item['Num_Securities']}</td>
            </tr>
            """
        
        table = f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Asset Class</th>
                    <th>Total NAV</th>
                    <th>% of Portfolio</th>
                    <th>Number of Securities</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
        
        return table
    
    def _generate_performance_table(self):
        """Generate HTML table for performance data."""
        performance = self.data['performance_by_asset_class']
        
        rows = ""
        for item in performance:
            return_class = 'positive' if item['Return_Pct'] >= 0 else 'negative'
            rows += f"""
            <tr>
                <td><strong>{item['Asset_Class']}</strong></td>
                <td>${item['End_NAV']/1e9:.3f}B</td>
                <td class="{return_class}">{item['Return_Pct']:.2f}%</td>
                <td>${item['Net_Investment_Income']/1e6:.2f}M</td>
                <td>${item['Contributions']/1e6:.2f}M</td>
                <td>${item['Distributions']/1e6:.2f}M</td>
            </tr>
            """
        
        table = f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Asset Class</th>
                    <th>Ending NAV</th>
                    <th>Return %</th>
                    <th>Investment Income</th>
                    <th>Contributions</th>
                    <th>Distributions</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
        
        return table
    
    def save_dashboard(self, output_path):
        """Save the dashboard to an HTML file."""
        html = self.generate_html()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\nDashboard saved successfully to: {output_path}")


def main(file_path: str = "FRL_Portfolio - Interview Use.xlsx",
         output_path: str = "alternatives_dashboard.html"):
    print("=" * 60)
    print("Fortitude Re - Alternatives Portfolio Dashboard Generator")
    print("=" * 60)

    print(f"\nUsing portfolio file: {file_path}")
    processor = PortfolioDataProcessor(file_path)
    processor.load_data()
    processor.classify_investments()

    data = processor.export_to_json()

    print("\nGenerating dashboard...")
    generator = DashboardGenerator(data)
    generator.save_dashboard(output_path)

    print("\n" + "=" * 60)
    print("Dashboard generation complete!")
    print("=" * 60)
    print(f"\nTo view the dashboard, open: {output_path}")
    print("=" * 60)



if __name__ == "__main__":
    main()
