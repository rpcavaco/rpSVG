
# aAzer 'activate' do venv primeiro

# Verificar que o este package está em editable install
#
# Fazer pip list' e confirmar a existência da linha:
# 
# 		rpSVG            0.9.0   /mnt/Dados/DEVC/SVG/rpSVG_package/src

# CAso contrário, não esquecer de fazer python -m pip install -e . na raiz do projecto
#  para instalar este package em modo 'editable'


cd tests
pytest
cd ..
