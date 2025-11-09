"""
EthniData v2.0.0 - Statistical Graphs Generator
Generates visualization graphs for v2.0.0 announcement
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Create images directory
OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

# Color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#D73F09',
    'islam': '#2ECC71',
    'christianity': '#3498DB',
    'hinduism': '#E74C3C',
    'buddhism': '#F39C12',
    'judaism': '#9B59B6',
    'europe': '#3498DB',
    'americas': '#E74C3C',
    'asia': '#F39C12',
    'africa': '#2ECC71',
    'oceania': '#9B59B6'
}

# Data
V1_STATS = {
    'records': 220656,
    'countries': 165,
    'languages': 46,
    'islam': 2811,
    'hinduism': 171,
    'buddhism': 490,
    'judaism': 3489,
    'christianity': 209502,
    'asia': 2715,
    'africa': 1637,
    'oceania': 476,
    'europe': 96927,
    'americas': 117264
}

V2_STATS = {
    'records': 415734,
    'countries': 238,
    'languages': 72,
    'islam': 69729,
    'hinduism': 3942,
    'buddhism': 6888,
    'judaism': 4850,
    'christianity': 122247,
    'asia': 58659,
    'africa': 55683,
    'oceania': 8185,
    'europe': 156215,
    'americas': 134481
}

def set_style():
    """Set global matplotlib style"""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.titleweight'] = 'bold'

def graph1_stats_card():
    """Main stats card - v1.3.0 vs v2.0.0"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    # Title
    fig.suptitle('EthniData v2.0.0 - MASSIVE UPDATE! 🔥',
                 fontsize=20, fontweight='bold', y=0.95)

    # Stats comparison
    stats = [
        ('Total Records', V1_STATS['records'], V2_STATS['records'], '+88%'),
        ('Countries', V1_STATS['countries'], V2_STATS['countries'], '+44%'),
        ('Languages', V1_STATS['languages'], V2_STATS['languages'], '+57%'),
    ]

    y_pos = 0.75
    for label, v1, v2, change in stats:
        ax.text(0.1, y_pos, label, fontsize=14, fontweight='bold')
        ax.text(0.4, y_pos, f'{v1:,}', fontsize=13, color='gray')
        ax.text(0.5, y_pos, '→', fontsize=13)
        ax.text(0.6, y_pos, f'{v2:,}', fontsize=13, fontweight='bold',
                color=COLORS['success'])
        ax.text(0.8, y_pos, change, fontsize=13, fontweight='bold',
                color=COLORS['accent'])
        y_pos -= 0.15

    # Installation command
    ax.text(0.5, 0.1, 'pip install --upgrade ethnidata',
            fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor=COLORS['primary'],
                     alpha=0.8, edgecolor='none'),
            color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '01_stats_card.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"✅ Generated: {OUTPUT_DIR / '01_stats_card.png'}")
    plt.close()

def graph2_religion_comparison():
    """Religion growth comparison"""
    fig, ax = plt.subplots(figsize=(12, 8))

    religions = ['Islam', 'Hinduism', 'Buddhism', 'Judaism', 'Christianity']
    v1_data = [V1_STATS['islam'], V1_STATS['hinduism'], V1_STATS['buddhism'],
               V1_STATS['judaism'], V1_STATS['christianity']]
    v2_data = [V2_STATS['islam'], V2_STATS['hinduism'], V2_STATS['buddhism'],
               V2_STATS['judaism'], V2_STATS['christianity']]

    x = np.arange(len(religions))
    width = 0.35

    bars1 = ax.bar(x - width/2, v1_data, width, label='v1.3.0',
                   color='lightgray', edgecolor='gray', linewidth=1.5)
    bars2 = ax.bar(x + width/2, v2_data, width, label='v2.0.0',
                   color=[COLORS['islam'], COLORS['hinduism'], COLORS['buddhism'],
                         COLORS['judaism'], COLORS['christianity']],
                   edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Calculate and display percentage increase
    increases = [
        (v2_data[i] - v1_data[i]) / v1_data[i] * 100
        for i in range(len(religions))
    ]

    for i, inc in enumerate(increases):
        ax.text(i, max(v1_data[i], v2_data[i]) * 1.15,
               f'+{int(inc)}%', ha='center',
               fontsize=11, fontweight='bold', color=COLORS['accent'])

    ax.set_xlabel('Religion', fontsize=13, fontweight='bold')
    ax.set_ylabel('Number of Records', fontsize=13, fontweight='bold')
    ax.set_title('Religious Coverage Improvement - v1.3.0 vs v2.0.0',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(religions, fontsize=12)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '02_religion_comparison.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '02_religion_comparison.png'}")
    plt.close()

def graph3_regional_distribution():
    """Regional distribution pie charts - Before & After"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    regions = ['Europe', 'Americas', 'Asia', 'Africa', 'Oceania']
    colors_list = [COLORS['europe'], COLORS['americas'], COLORS['asia'],
                   COLORS['africa'], COLORS['oceania']]

    # v1.3.0
    v1_data = [V1_STATS['europe'], V1_STATS['americas'], V1_STATS['asia'],
               V1_STATS['africa'], V1_STATS['oceania']]
    v1_percentages = [x/sum(v1_data)*100 for x in v1_data]

    wedges1, texts1, autotexts1 = ax1.pie(v1_data, labels=regions, autopct='%1.1f%%',
                                           colors=colors_list, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'},
                                           explode=(0.05, 0.05, 0, 0, 0))

    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax1.set_title('v1.3.0 - Imbalanced\n❌ Asia: 1.2% | Africa: 0.7%',
                 fontsize=14, fontweight='bold', pad=20)

    # v2.0.0
    v2_data = [V2_STATS['europe'], V2_STATS['americas'], V2_STATS['asia'],
               V2_STATS['africa'], V2_STATS['oceania']]
    v2_percentages = [x/sum(v2_data)*100 for x in v2_data]

    wedges2, texts2, autotexts2 = ax2.pie(v2_data, labels=regions, autopct='%1.1f%%',
                                           colors=colors_list, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})

    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')

    ax2.set_title('v2.0.0 - Balanced\n✅ Asia: 14.1% | Africa: 13.4%',
                 fontsize=14, fontweight='bold', pad=20, color=COLORS['success'])

    fig.suptitle('Regional Distribution Improvement',
                fontsize=18, fontweight='bold', y=0.98)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '03_regional_distribution.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '03_regional_distribution.png'}")
    plt.close()

def graph4_regional_growth():
    """Regional growth multipliers"""
    fig, ax = plt.subplots(figsize=(12, 7))

    regions = ['Asia', 'Africa', 'Oceania', 'Europe', 'Americas']
    multipliers = [
        V2_STATS['asia'] / V1_STATS['asia'],
        V2_STATS['africa'] / V1_STATS['africa'],
        V2_STATS['oceania'] / V1_STATS['oceania'],
        V2_STATS['europe'] / V1_STATS['europe'],
        V2_STATS['americas'] / V1_STATS['americas']
    ]

    colors_bars = [COLORS['asia'], COLORS['africa'], COLORS['oceania'],
                   COLORS['europe'], COLORS['americas']]

    bars = ax.barh(regions, multipliers, color=colors_bars,
                   edgecolor='black', linewidth=2)

    # Add value labels
    for i, (bar, mult) in enumerate(zip(bars, multipliers)):
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
               f'{mult:.1f}x', ha='left', va='center',
               fontsize=13, fontweight='bold')

    # Add v1 and v2 record counts
    for i, region in enumerate(regions):
        region_lower = region.lower()
        v1 = V1_STATS[region_lower]
        v2 = V2_STATS[region_lower]
        ax.text(0.2, i, f'{v1:,} → {v2:,}', ha='left', va='center',
               fontsize=10, color='white', fontweight='bold')

    ax.set_xlabel('Growth Multiplier', fontsize=13, fontweight='bold')
    ax.set_title('Regional Coverage Growth - How Many Times More Data?',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, max(multipliers) + 2)
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '04_regional_growth.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '04_regional_growth.png'}")
    plt.close()

def graph5_religion_percentage_change():
    """Religion percentage change visualization"""
    fig, ax = plt.subplots(figsize=(12, 8))

    religions = ['Islam', 'Hinduism', 'Buddhism', 'Judaism']
    v1_data = [V1_STATS['islam'], V1_STATS['hinduism'],
               V1_STATS['buddhism'], V1_STATS['judaism']]
    v2_data = [V2_STATS['islam'], V2_STATS['hinduism'],
               V2_STATS['buddhism'], V2_STATS['judaism']]

    percentage_changes = [
        (v2 - v1) / v1 * 100
        for v1, v2 in zip(v1_data, v2_data)
    ]

    colors_bars = [COLORS['islam'], COLORS['hinduism'],
                   COLORS['buddhism'], COLORS['judaism']]

    bars = ax.bar(religions, percentage_changes, color=colors_bars,
                  edgecolor='black', linewidth=2, width=0.6)

    # Add value labels
    for bar, pct in zip(bars, percentage_changes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
               f'+{int(pct):,}%', ha='center', va='bottom',
               fontsize=14, fontweight='bold', color=COLORS['accent'])

    # Add emoji labels
    emojis = ['🌙', '🕉️', '☸️', '✡️']
    for i, (bar, emoji) in enumerate(zip(bars, emojis)):
        ax.text(bar.get_x() + bar.get_width()/2., -200,
               emoji, ha='center', va='top', fontsize=24)

    ax.set_ylabel('Percentage Increase (%)', fontsize=13, fontweight='bold')
    ax.set_title('Religious Data Expansion - Percentage Growth',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(percentage_changes) + 300)
    ax.grid(axis='y', alpha=0.3)

    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}%'))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '05_religion_percentage_change.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '05_religion_percentage_change.png'}")
    plt.close()

def graph6_overall_comparison():
    """Overall statistics comparison"""
    fig, ax = plt.subplots(figsize=(10, 8))

    categories = ['Total\nRecords', 'Countries', 'Languages',
                  'Database\nSize (MB)']
    v1_values = [220656, 165, 46, 19]
    v2_values = [415734, 238, 72, 75]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, v1_values, width, label='v1.3.0',
                   color='lightgray', edgecolor='gray', linewidth=2)
    bars2 = ax.bar(x + width/2, v2_values, width, label='v2.0.0',
                   color=COLORS['primary'], edgecolor='black', linewidth=2)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            label = f'{int(height):,}' if height > 100 else f'{int(height)}'
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   label, ha='center', va='bottom',
                   fontsize=11, fontweight='bold')

    # Add percentage increase
    increases = [(v2_values[i] - v1_values[i]) / v1_values[i] * 100
                 for i in range(len(categories))]

    for i, inc in enumerate(increases):
        ax.text(i, max(v1_values[i], v2_values[i]) * 1.15,
               f'+{int(inc)}%', ha='center',
               fontsize=12, fontweight='bold', color=COLORS['accent'])

    ax.set_ylabel('Value', fontsize=13, fontweight='bold')
    ax.set_title('EthniData v1.3.0 vs v2.0.0 - Overall Comparison',
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '06_overall_comparison.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '06_overall_comparison.png'}")
    plt.close()

def graph7_key_improvements():
    """Key improvements summary card"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    # Title
    fig.suptitle('EthniData v2.0.0 - Key Improvements',
                 fontsize=20, fontweight='bold', y=0.95)

    improvements = [
        ('🔥 Total Records', '220K → 415K', '+88%'),
        ('🌍 Countries', '165 → 238', '+44%'),
        ('🗣️  Languages', '46 → 72', '+57%'),
        ('', '', ''),  # spacer
        ('🌙 Islam Coverage', '2.8K → 69.7K', '+2,380%'),
        ('🕉️ Hinduism Coverage', '171 → 3.9K', '+2,205%'),
        ('☸️  Buddhism Coverage', '490 → 6.9K', '+1,306%'),
        ('', '', ''),  # spacer
        ('🌏 Asia Coverage', '1.2% → 14.1%', '11.7x'),
        ('🌍 Africa Coverage', '0.7% → 13.4%', '19x'),
        ('🌊 Oceania Coverage', '0.2% → 2.0%', '10x'),
    ]

    y_pos = 0.85
    for label, change, metric in improvements:
        if not label:  # spacer
            y_pos -= 0.05
            continue

        ax.text(0.05, y_pos, label, fontsize=13, fontweight='bold')
        ax.text(0.45, y_pos, change, fontsize=12, color='gray')

        # Highlight the metric
        bbox_props = dict(boxstyle='round,pad=0.3',
                         facecolor=COLORS['accent'],
                         alpha=0.8, edgecolor='none')
        ax.text(0.85, y_pos, metric, fontsize=12, fontweight='bold',
                bbox=bbox_props, color='white', ha='center')

        y_pos -= 0.08

    # Footer
    ax.text(0.5, 0.05, 'pip install --upgrade ethnidata',
            fontsize=13, ha='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor=COLORS['primary'],
                     alpha=0.9, edgecolor='none'),
            color='white', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '07_key_improvements.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {OUTPUT_DIR / '07_key_improvements.png'}")
    plt.close()

def main():
    """Generate all graphs"""
    print("\n🎨 EthniData v2.0.0 - Generating Statistical Graphs...\n")

    set_style()

    graph1_stats_card()
    graph2_religion_comparison()
    graph3_regional_distribution()
    graph4_regional_growth()
    graph5_religion_percentage_change()
    graph6_overall_comparison()
    graph7_key_improvements()

    print(f"\n✅ All graphs generated successfully!")
    print(f"📁 Location: {OUTPUT_DIR}")
    print(f"\n📊 Generated {len(list(OUTPUT_DIR.glob('*.png')))} images:")
    for img in sorted(OUTPUT_DIR.glob('*.png')):
        print(f"   - {img.name}")

if __name__ == '__main__':
    main()
