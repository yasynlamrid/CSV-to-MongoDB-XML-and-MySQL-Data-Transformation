import pymongo
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from lxml import etree
import mysql.connector



# ---------------------- Extraire des données de MongoDB sous forme d'un fichier XML -----------------------------------


# Connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.Nuclear_Explosion2
collection = db.Nuclear_Explosion2

# Chercher et extraire les données de MongoDB
donnees_mongodb = collection.find()

# Création de l'élément racine XML
root = ET.Element("nuclear_explosions")

# Parcourir la liste des données stocker
for document in donnees_mongodb:
    # Création de l'élément pour chaque document
    element = ET.Element("nuclear_explosion".lower())

    element.set("_id", str(document["_id"]))

    WEAPON_SOURCE_COUNTRY = ET.Element("WEAPON_SOURCE_COUNTRY".lower())
    WEAPON_SOURCE_COUNTRY.text = document.get("WEAPON_SOURCE_COUNTRY", "")
    element.append(WEAPON_SOURCE_COUNTRY)

    WEAPON_DEPLOYMENT_LOCATION = ET.Element("WEAPON_DEPLOYMENT_LOCATION".lower())
    WEAPON_DEPLOYMENT_LOCATION.text = document.get("WEAPON_DEPLOYMENT_LOCATION", "")
    element.append(WEAPON_DEPLOYMENT_LOCATION)

    data_element = ET.Element("Data".lower())
    element.append(data_element)

    data = document.get("Data", {})

    source = ET.Element("Source".lower())
    source.text = data.get("Source", "")
    data_element.append(source)

    magnitude = ET.Element("Magnitude".lower())
    data_element.append(magnitude)

    body = ET.Element("Body".lower())
    body.text = str(data.get("Magnitude", {}).get("Body", ""))
    magnitude.append(body)

    surface = ET.Element("surface".lower())
    surface.text = str(data.get("Magnitude", {}).get("Surface", ""))
    magnitude.append(surface)

    yeild = ET.Element("Yeild".lower())
    data_element.append(yeild)

    lower = ET.Element("Lower".lower())
    lower.text = str(data.get("Yeild", {}).get("Lower", ""))
    yeild.append(lower)

    upper = ET.Element("Upper".lower())
    upper.text = str(data.get("Yeild", {}).get("Upper", ""))
    yeild.append(upper)

    purpose = ET.Element("Purpose".lower())
    purpose.text = data.get("Purpose", "")
    data_element.append(purpose)

    name = ET.Element("Name".lower())
    name.text = data.get("Name", "")
    data_element.append(name)

    type_element = ET.Element("Type".lower())
    type_element.text = data.get("Type", "")
    data_element.append(type_element)

    location = ET.Element("Location".lower())
    element.append(location)

    coordinates = ET.Element("Coordinates".lower())
    location.append(coordinates)

    latitude = ET.Element("Latitude".lower())
    latitude.text = str(document.get("Location", {}).get("Cordinates", {}).get("Latitude", ""))
    coordinates.append(latitude)

    longitude = ET.Element("Longitude".lower())
    longitude.text = str(document.get("Location", {}).get("Cordinates", {}).get("Longitude", ""))
    coordinates.append(longitude)

    depth = ET.Element("Depth".lower())
    depth.text = str(document.get("Location", {}).get("Cordinates", {}).get("Depth", ""))
    coordinates.append(depth)

    date = ET.Element("Date".lower())
    element.append(date)

    day = ET.Element("Day".lower())
    day.text = str(document.get("Date", {}).get("Day", ""))
    date.append(day)

    month = ET.Element("Month".lower())
    month.text = str(document.get("Date", {}).get("Month", ""))
    date.append(month)

    year = ET.Element("Year".lower())
    year.text = str(document.get("Date", {}).get("Year", ""))
    date.append(year)

    root.append(element)


# Génération du fichier XML bien formé

tree = ET.ElementTree(root)
xml_string = ET.tostring(root, encoding="unicode")
xml_string = xml_string.replace("><", ">\n<")


dom = minidom.parseString(xml_string)
formatted_xml = dom.toprettyxml(indent="  ", newl='')

# Écrire le fichier XML formatté
with open("XML_Nuclear_Explosions.xml", "w", encoding="utf-8") as xml_file:
    xml_file.write(formatted_xml)

# Fermeture de la connexion à MongoDB
client.close()

print("Le XML a été généré avec succès")

# ---------------------------------------- Validation du fichier xml par XSD-----------------------------------------#

# Déclaration des fichiers XML et XSD
xml_file = "XML_Nuclear_Explosions.xml"
xsd_file = "XSD_Nuclear_Explosions.xsd"

xmlschema_doc = etree.parse(xsd_file)
xmlschema = etree.XMLSchema(xmlschema_doc)

# Charger le fichier XML à valider
xml_doc = etree.parse(xml_file)

# Valider le fichier XML par rapport au schéma XSD
if xmlschema.validate(xml_doc):
    print("Le fichier XML est validé par rapport au schéma XSD")
else:
    print("Le fichier XML n'est pas valide par rapport au schéma XSD")
    validation_errors = xmlschema.error_log
    for error in validation_errors:
        print(f"Erreur à la ligne {error.line}: {error.message}")

# ------------------------------ Fusionner les fichiers XML avec  XSLT --------------------------------#

# Charger le fichier XML
xml_file = "XML_Nuclear_Explosions.xml"
xml_tree = etree.parse(xml_file)

# Charger le fichier XSLT
xslt_file = "XSLT_Nuclear_Explosions.xslt"
xslt_tree = etree.parse(xslt_file)

# Créer un transformateur XSLT
transform = etree.XSLT(xslt_tree)

# Appliquer la transformation
result_tree = transform(xml_tree)

# Ajouter un lien vers la feuille de style CSS
html_root = result_tree.getroot()
head = html_root.find(".//head")
link_element = etree.Element("link")
link_element.set("rel", "stylesheet")
link_element.set("type", "text/css")
link_element.set("href", "CSS_nuclear_explosions.css")
head.append(link_element)

# Sauvegarder le résultat dans un fichier HTML
result_file = "Xhtml_Nuclear_explosions.html"
with open(result_file, "wb") as output_file:
    output_file.write(etree.tostring(result_tree, pretty_print=True, encoding="UTF-8"))

print("La transformation a été effectuée avec succès. Le résultat a été sauvegardé dans", result_file)


# ----------------------- Injecter le fichier Xml dans la base de données Mysql ---------------------------#



# Connexion à la base de données MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yassin@1994",
    database="nuclear_explosions_db"
)
# Créez un curseur pour exécuter les requêtes SQL
cursor = db_connection.cursor()

# Les deux lignes suivantes permettent  de supprimer la table existante si elle existe
cursor.execute("DROP TABLE IF EXISTS nuclear_explosions")
cursor.execute("DROP TABLE IF EXISTS source")

# Creation de la table enfant (source) avec les valeurs possibles de l'élément source
create_child_table = """
CREATE TABLE source (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(255)
)
"""

cursor.execute(create_child_table)

# Creation de la table parent (nuclear_explosions) avec la clé étrangère
create_parent_table = """
CREATE TABLE nuclear_explosions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    weapon_source_country VARCHAR(255),
    weapon_deployment_location VARCHAR(255),
    name VARCHAR(255),
    type VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    depth FLOAT,
    day INT,
    month INT,
    year INT,
    source_id INT,
    FOREIGN KEY (source_id) REFERENCES source(id)
)
"""
cursor.execute(create_parent_table)

# Les valeurs possibles de l'élément source dans la table enfant
source_values = ["MTM", "DOE", "UGS", "DIS", "ISC"]
insert_source_values = "INSERT INTO source (source_name) VALUES (%s)"
for value in source_values:
    cursor.execute(insert_source_values, (value,))

# Insertion les données dans les tables parent et enfant
tree = ET.parse('XML_Nuclear_Explosions.xml')
root = tree.getroot()

for explosion in root.findall('nuclear_explosion'):
    weapon_source_country = explosion.find('weapon_source_country').text
    weapon_deployment_location = explosion.find('weapon_deployment_location').text
    name = explosion.find('data/name').text
    type = explosion.find('data/type').text
    latitude = float(explosion.find('location/coordinates/latitude').text)
    longitude = float(explosion.find('location/coordinates/longitude').text)
    depth = float(explosion.find('location/coordinates/depth').text)
    day = int(explosion.find('date/day').text)
    month = int(explosion.find('date/month').text)
    year = int(explosion.find('date/year').text)
    source_name = explosion.find('data/source').text

    # Insertion les données dans la table parent
    insert_parent_data = """
    INSERT INTO nuclear_explosions 
    (weapon_source_country, weapon_deployment_location, name, type, latitude, longitude, depth, day, month, year, source_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT id FROM source WHERE source_name = %s))
    """
    cursor.execute(insert_parent_data, (weapon_source_country, weapon_deployment_location, name, type, latitude, longitude, depth, day, month, year, source_name))

# validation les changements dans la base de données
db_connection.commit()

# fin de la connexion à la base de données
cursor.close()
db_connection.close()

print("Données insérées avec succès dans la base de données.")