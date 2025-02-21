conda --version
conda env list

# create new environment called learn-langchain
conda create -n <ENV_NAME> python
conda install -n <ENV_NAME> learn-langchain
conda activate <ENV_NAME>
conda create -n <ENV_NAME> python=3.11 scipy=0.17.3 astroid babel
conda create -n llm python=3.12
conda install -n llm ipython jupyter

# Listing dependencies
conda list -n ice_breaker
conda list 

# Install dependency
#conda install langchain
conda install black
conda install python-dotenv
conda install conda-forge::langchain
conda install conda-forge::langchain-openai
conda install conda-forge::langchain-community
conda install conda-forge::langchainhub
conda install langchain-ollama

pip install langchain-ollama

pip list

conda remove -n <ENV_NAME> --all

# Clone an existing environment
conda create --name clone_envname --clone envname

# for requirement text
pip install -e .



conda deactivate
conda remove --name ENV_NAME --all