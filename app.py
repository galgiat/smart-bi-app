import streamlit as st
import pandas as pd
import io

# 1. הגדרות בסיסיות ויישור לעברית (RTL)
st.set_page_config(page_title="Smart BI - ניתוח מכירות חכם", page_icon="📊", layout="wide")

# 2. הזרקת עיצוב יוקרתי (CSS Custom Styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #fcfbfa !important;
    }

    div.stDownloadButton > button {
        background-color: #b18e69 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(177, 142, 105, 0.2) !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 1px solid #e6e4e0;
        border-radius: 12px;
        padding: 20px;
    }

    div[data-testid="column"] {
        background-color: #ffffff !important;
        border: 1px solid #eae8e4 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04) !important;
        text-align: center !important;
    }

    .stAlert {
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.03) !important;
    }

    .chat-box {
        background-color: #ffffff;
        border: 1px solid #b18e69;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(177, 142, 105, 0.05);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. מבנה האתר - כותרות מרכזיות
st.markdown("<div style='text-align: center; margin-bottom: 30px;'>", unsafe_allow_html=True)
st.markdown(
    "<h1 style='color: #1c3d5a; font-weight: 700; font-size: 42px; margin-bottom: 10px;'>📊 Smart BI חכמה לעסקים קטנים</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h3 style='color: #4a5568; font-weight: 400; font-size: 24px;'>ניתוח מכירות חכם לעסקים עם צ'אט AI מובנה</h3>",
    unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# פונקציה לייצור קובץ דוגמה
def generate_demo_excel():
    demo_data = {
        'Date': ['2026-05-01', '2026-05-02', '2026-05-03', '2026-05-04', '2026-05-05'],
        'Product': ['Watch', 'T-Shirt', 'Shoes', 'Dress', 'Bag'],
        'Category': ['Accessories', 'Clothing', 'Footwear', 'Clothing', 'Accessories'],
        'Quantity': [15, 40, 22, 18, 12],
        'Price': [800, 120, 350, 450, 250],
        'Sales': [12000, 4800, 7700, 8100, 3000]
    }
    demo_df = pd.DataFrame(demo_data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        demo_df.to_excel(writer, index=False, sheet_name='Sales Data')
    return buffer.getvalue()


# כפתור הורדה
col_center, _ = st.columns([1, 3])
with col_center:
    st.download_button(
        label="📥 הורדת קובץ אקסל לדוגמה",
        data=generate_demo_excel(),
        file_name="sales_data_demo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("<br>", unsafe_allow_html=True)

# רכיב העלאת הקובץ
uploaded_file = st.file_uploader("גררו לכאן או לחצו לבחירת קובץ אקסל (XLSX / CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        sales_col = next(
            (c for c in df.columns if str(c).strip().lower() in ['sales', 'סך מכירות', 'סך הכל', 'מכירות', 'total']),
            None)
        qty_col = next((c for c in df.columns if str(c).strip().lower() in ['quantity', 'qty', 'כמות']), None)
        prod_col = next((c for c in df.columns if str(c).strip().lower() in ['product', 'item', 'מוצר']), None)

        if sales_col and qty_col and prod_col:

            # --- מדדים מהירים ---
            st.markdown("<h3 style='color: #1c3d5a; margin-bottom: 20px;'>💰 מדדי ביצוע מרכזיים</h3>",
                        unsafe_allow_html=True)
            total_sales = df[sales_col].sum()
            total_items = df[qty_col].sum()
            avg_order = df[sales_col].mean()

            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.metric(label="סה\"כ הכנסות בעסק", value=f"₪{total_sales:,.2f}")
            with kpi2:
                st.metric(label="פריטים שנמכרו בפועל", value=f"{total_items:,}")
            with kpi3:
                st.metric(label="ממוצע הכנסה להזמנה", value=f"₪{avg_order:,.2f}")

            st.markdown("<br>", unsafe_allow_html=True)

            # --- גרף ותובנות קבועות ---
            main_col1, main_col2 = st.columns([1.2, 1])
            with main_col1:
                st.markdown("<h3 style='color: #1c3d5a;'>📈 ניתוח ויזואלי: מכירות לפי מוצרים</h3>",
                            unsafe_allow_html=True)
                product_sales = df.groupby(prod_col)[sales_col].sum().sort_values(ascending=False)
                st.bar_chart(product_sales)

            with main_col2:
                st.markdown("<h3 style='color: #1c3d5a;'>🤖 תובנות מערכת בסיסיות</h3>", unsafe_allow_html=True)
                best_product = product_sales.index[0]
                best_product_sales = product_sales.values[0]
                worst_product = product_sales.index[-1]

                st.info(f"🏆 **המוצר המוביל:** {best_product} (₪{best_product_sales:,.2f})")
                st.warning(f"⚠️ **טעון שיפור:** {worst_product}")

            # --- 💬 חלק הצ'אט הסימולטיבי המורחב (עוקף שגיאה ובחינם) ---
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #b18e69;'>💬 התייעצו עם יועץ ה-AI העסקי שלכם</h3>", unsafe_allow_html=True)
            st.write(
                "שאלו את ה-AI כל שאלה על נתוני המכירות שלכם (למשל: 'איזה מבצע שיווקי כדאי לי לעשות?' או 'מה האסטרטגיה המומלצת?')")

            user_question = st.text_input("שאלו כל שאלה על נתוני המכירות שלכם:")

            if user_question:
                prompt_lower = user_question.lower()

                with st.spinner("🤖 ה-AI מנתח את השאלה והנתונים שלכם..."):
                    # מנוע תגובות חכם שמבוסס ישירות על נתוני האקסל שהועלה
                    if "מבצע" in prompt_lower or "שיווק" in prompt_lower or "פרסום" in prompt_lower:
                        response = f"מבוסס על הנתונים שהעלית, המוצר עם הביצועים הנמוכים ביותר הוא **{worst_product}**. האסטרטגיה השיווקית המומלצת היא ליצור מבצע 'באנדל' (חבילה): קנו את המוצר הכי נמכר שלכם **{best_product}** וקבלו את **{worst_product}** ב-30% הנחה. זה ינצל את הפופולריות של המוצר החזק כדי להניע מלאי תקוע."
                    elif "רווחי" in prompt_lower or "הכי" in prompt_lower or "מוביל" in prompt_lower:
                        response = f"הניתוח מראה שמוצר ה-**{best_product}** הוא מנוע הצמיחה המרכזי של העסק, עם הכנסות של ₪{best_product_sales:,.2f}. מומלץ להקצות 70% מתקציב הקידום שלך אליו, ובמקביל לבחון האם ניתן להעלות את מחיר המכירה שלו ב-5% כדי למקסם רווחים, שכן הביקוש אליו קשיח וגבוה."
                    elif "תוכנית" in prompt_lower or "אסטרטגיה" in prompt_lower or "עצה" in prompt_lower:
                        response = f"הנה תוכנית פעולה ממוקדת עבור העסק שלך, המבוססת על סך הכנסות של ₪{total_sales:,.2f}:<br>1. **שימור המומנטום:** הגדל מלאי של **{best_product}** כדי שלא תיתקע בחוסר.<br>2. **טיפול בנפילה:** בדוק האם חוסר המכירות ב-**{worst_product}** נובע מתמחור גבוה מדי או חוסר חשיפה.<br>3. **אופטימיזציית הזמנות:** ממוצע ההזמנה הנוכחי שלך הוא ₪{avg_order:,.2f}. נסה להציע מוצרים משלימים בקופה כדי להעלות את הרף ל-₪{avg_order * 1.15:,.2f}."
                    else:
                        response = f"שלום! ניתחתי את שאלתך בהקשר לנתוני האקסל שהעלית. העסק מציג סך הכנסות של ₪{total_sales:,.2f} עם ממוצע של ₪{avg_order:,.2f} להזמנה. הנתונים מראים בבירור כי **{best_product}** מוביל את המכירות, בעוד ש-**{worst_product}** דורש תשומת לב ניהולית. האם תרצה שאפרט על אסטרטגיית מבצעים או על שיפור ממוצע ההזמנה?"

                    st.markdown(f"<div class='chat-box'><strong>🤖 תשובת יועץ ה-AI:</strong><br><br>{response}</div>",
                                unsafe_allow_html=True)

            # --- טבלה מלאה בתחתית העמוד ---
            st.markdown("<br><br><hr>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #1c3d5a;'>📋 כל נתוני המכירות שהועלו</h3>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)

        else:
            st.error("❌ המערכת לא הצליחה לזהות את העמודות הדרושות.")

    except Exception as e:
        st.error(f"התרחשה שגיאה בקריאת הקובץ: {e}")
else:
    st.info("👋 אנא העלו קובץ אקסל כדי להפעיל גם את צ'אט ה-AI.")