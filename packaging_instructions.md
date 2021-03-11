# Packaging Instructions

É possível gerar um `snap` de uma aplicação Python diretamente, mas achei mais simples compilar usando [`PyInstaller`](https://pyinstaller.readthedocs.io/en/stable/) e tratar como um programa _standalone_. A vantagem é que o mesmo pacote pode ser usado para compilar em ambiente Windows e obter um executável.

O segundo passo é, naturalmente, gerar o `snap` através da `snapcraft`.

## PyInstaller

Vou usar o termo compilar inadequadamente para me referir ao processo de reunir todas as dependências do programa em uma única pasta e criar um arquivo executável que não depende das bibliotecas do sistema,exceto pela `glibc` que precisa ser compatível.

A dependência da `glibc` implica que o programa só pode ser executado em ambientes que possuam uma `glibc` equivalente ou mais recente do que o ambiente de compilação. A recomendação costuma ser compilar no [CentOS](http://isoredirect.centos.org/centos/7/isos/x86_64/) (uma máquina virtual é suficiente).

A seguir, vou descrever a configuração do CentOS 7, mas ela pode ser ignorada.

### Configurando o CentOS 7

Após instalar o CentOS (instalei a versão 7 _minimal_), é necessário instalar alguns pacotes.

```bash
sudo yum -y install epel-release
sudo yum -y install gcc make build-essentials python36-devel git cairo-gobject-devel python36-gobject gobject-instrospection-devel.x86_64 gtk3-devel
```

#### Acessando arquivos do _host_ a partir do _guest_

Usando o VirtualBox, é possível montar uma pasta do sistema _host_ direto no sistema _guest_, e isso vai ser importante para trafegar os arquivos, a menos que se usem outras alternativas.

Para isso, é necessário acessar o menu `Devices` > `Insert Guest Additions CD Image...`. Então montar e instalar o módulo:

```bash
$ sudo yum -y update
$ # wget café && watch rua
$ reboot # provavelmente haverá uma atualização do kernel, então isso é importante.
$ sudo yum -y bzip2 dkms perl binutils patch libgomp glibc-headers glibc-devel kernel-headers kernel-devel xorg-x11-drivers xorg-x11-utils
$ export KERN_DIR=/usr/src/kernels/$(uname -r)
$ sudo mkdir /mnt/vbox
$ sudo mount /dev/cdrom /mnt/vbox
$ sudo /mnt/vbox/VBoxLinuxAdditions.run
$ reboot
```

No menu do Virtual Box, acesse `Devices` > `Shared Folders` > `Shared Folders Settings...`. Adicione a pasta de interesse marcando _Auto Mount_ e ela será montada no ponto escolhido.

#### De volta ao programa

Com o código fonte disponível para o usuário na máquina virtual, um _environment_ precisa ser criado seguido da instalação das dependências:

```bash
$ python3 -m venv env
$ source ./env/bin/activate
(env) $ pip install --upgrade pip
(env) $ pip install -r requirements.txt
(env) $ pip install pyinstaller
```

Nesse ponto, o CentOS 7 está configurado para o _build_.

### Gerando o executável

Simplesmente execute o arquivo `pyinstaller.sh`.

```bash
pyinstaller ./GUI/main.py --name qsarmodeling \
    --hidden-import cmath \
    --hidden-import sklearn.utils._weight_vector \
    --hidden-import pandas \
    --add-data "./GUI/Views/main.glade:Views" \
    --add-data "./GUI/Views/ga.glade:Views" \
    --add-data "./GUI/Views/ops.glade:Views" \
    --add-data "./GUI/Views/about.glade:Views" \
    --add-data "./GUI/Views/varcut.glade:Views" \
    --add-data "./GUI/Views/corrcut.glade:Views" \
    --add-data "./GUI/Views/autocorrcut.glade:Views" \
    --add-data "./GUI/Views/cross_validation.glade:Views" \
    --add-data "./GUI/Views/yrlno.glade:Views" \
    --noconfirm
```

As instruções `hidden-import` servem para corrigir quando o PyInstaller não consegue ver os imports. Compilei várias vezes, adicionando uma nova flag sempre que algum pacote faltava.

As flags `add-data` servem para adicionar arquivos estáticos e o que há após os `:` é o diretório no qual o arquivo será colocado, no _bundle_ final.

Após executar o _script_, se nada der errado, uma pasta `./dist` estará disponível.

Comprimindo tudo para gerar o `snap`:

```bash
(env) $ tar -C ./dist/qsarmodeling -cJf qsarmodeling.tar.xz $(ls ./dist/qsarmodeling)
```

> A compressão pode ser feita para `.zip`, mas isso implicará num snap maior para o usuário final (embora com um tempo de compressão menor, sendo aceitável no estágio de desenvolvimento).

## Snapcraft

De volta à maquina real, é necessário instalar o `snapcraft` para gerar o `snap`.

```bash
$ sudo snap install snapcraft --classic
```

Veja o [Quickstart Guide](https://snapcraft.io/docs/snapcraft-overview) e os arquivos `setup.py`, `snapcraft.yaml` e `pyproject.toml` na raiz do projeto.
