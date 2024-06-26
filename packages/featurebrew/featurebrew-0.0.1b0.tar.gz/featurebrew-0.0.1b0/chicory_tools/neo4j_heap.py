import json

from utils.helper import datetime_handler
from neo4j import GraphDatabase
from neo4j.debug import Watcher


class GraphService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, trust="TRUST_ALL_CERTIFICATES")

    def close(self):
        self.driver.close()

    def create_node(self, label, **properties):
        try:
            # with Watcher("neo4j"):
            with self.driver.session() as session:
                session.write_transaction(self._create_bean_tx, label, properties)
        except Exception as e:
            print (e)

    def create_node_dict(self, label, dict_props, region):
        try:
            # Serialize nested dictionaries
            for key, value in dict_props.items():
                if isinstance(value, dict) or isinstance(value, list):
                    dict_props[key] = json.dumps(value, default=datetime_handler)
            dict_props['region'] = region
            # with Watcher("neo4j"):
            with self.driver.session() as session:
                session.write_transaction(self._create_bean_dict_tx, label, dict_props)
        except Exception as e:
            print (e)


    def create_relation_by_id(self, label_a, property_a, label_b, property_b, relationship_type):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._create_blend_tx, "id", label_a, property_a, label_b, property_b, relationship_type)
        except Exception as e:
            print (e)

    def create_relation_by_name(self, label_a, property_a, label_b, property_b, relationship_type):
        try:
            with self.driver.session() as session:
                session.write_transaction(self._create_blend_tx, "name", label_a, property_a, label_b, property_b, relationship_type)
        except Exception as e:
            print (e)

    @staticmethod
    def _create_node_tx(tx, label, properties):
        query = (
            f"CREATE (a:{label} $properties) "
            "RETURN id(a)"
        )
        result = tx.run(query, properties=properties)
        return result.single()[0]

    @staticmethod
    def _create_node_dict_tx(tx, label, properties):
        # Construct a Cypher query string with properties unpacked
        properties_string = ', '.join([f'{key}: ${key}' for key in properties.keys()])
        query = (
            f"CREATE (a:{label} {{{properties_string}}}) "
            "RETURN id(a)"
        )
        result = tx.run(query, **properties)
        return result.single()[0]


    @staticmethod
    def _create_relation_tx(tx, by, label_a, property_a, label_b, property_b, relationship_type):
        cypher_query = (
            f"MATCH (a:{label_a}), (b:{label_b}) "
            f"WHERE a.{by} = \"{property_a}\" AND b.{by} = \"{property_b}\" "
            f"CREATE (a)-[r:{relationship_type}]->(b) "
            "RETURN type(r)"
        )
        return tx.run(cypher_query, property_a=property_a, property_b=property_b)


    @staticmethod
    def _find_node_tx(tx, label, property_name, property_value):
        cypher_query = f"MATCH (n:{label} {{ {property_name}: $property_value }}) RETURN n"
        result = tx.run(cypher_query, property_value=property_value)
        return [record["n"] for record in result]


    @staticmethod
    def _update_node_tx(tx, label, identifying_property, new_properties):
        cypher_query = (
            f"MATCH (n:{label} {{ {identifying_property['name']}: $identifying_value }}) "
            "SET n += $new_properties "
            "RETURN n"
        )
        return tx.run(cypher_query, identifying_value=identifying_property['value'], new_properties=new_properties)


    @staticmethod
    def _delete_node_tx(tx, label, property_name, property_value):
        cypher_query = f"MATCH (n:{label} {{ {property_name}: $property_value }}) DETACH DELETE n"
        tx.run(cypher_query, property_value=property_value)

