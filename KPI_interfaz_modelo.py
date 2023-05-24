'''
    SECCION LOGO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
            col1.image('logo.png')
    with col2: 
            st.empty()

    '''
    SECCION KPI
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
    with col2:
        st.empty()
    with col3:
        st.empty()

    '''
    SECCION CUERPO
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown("<h1 style='font-size: 30px;'>KPI 1: Distribución de sismos por categoría de magnitud</h1>", unsafe_allow_html=True)
    with col2:
        st.empty()
    with col3:
        st.empty()
    
    '''
    SECCION FOOTER
    '''
    col1, col2, col3 = st.columns([0.55, 0.05, 0.4])
    with col1:
        st.markdown('<div class="EMPTY_footer"></div>', unsafe_allow_html=True)
        col1.image('logo_footer.png')
    with col2:
        st.empty()
