import sqlite3
from sqlite3 import Error
from typing import Union, Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import os


def DUDBC_RateWriter(databasepath):

    def create_connection(db_file):
        """ Create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn


    def create_tables(conn):
        """ Create all tables needed for the hierarchical data structure """

        # Drop tables if they exist (for development)
        drop_tables = [
            "Second_Inner_Data", "Second_Inner_Table",
            "Others", "Machines", "Materials", "Manpower",
            "First_Inner_Title", "First_Inner_Table",
            "Reference_Data_Items", "Reference_Data",
            "Title_Section_Data", "Title_Section",
            "Root"
        ]

        try:
            c = conn.cursor()
            for table in drop_tables:
                c.execute(f"DROP TABLE IF EXISTS {table}")
        except Error as e:
            print(f"Error dropping tables: {e}")

        # Create fresh tables
        sql_create_root_table = """CREATE TABLE IF NOT EXISTS Root (
                                    id INTEGER PRIMARY KEY
                                );"""

        sql_create_title_section_table = """CREATE TABLE IF NOT EXISTS Title_Section (
                                            id INTEGER PRIMARY KEY,
                                            root_id INTEGER NOT NULL,
                                            FOREIGN KEY (root_id) REFERENCES Root (id)
                                        );"""

        sql_create_title_section_data = """CREATE TABLE IF NOT EXISTS Title_Section_Data (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            title_section_id INTEGER NOT NULL,
                                            key TEXT NOT NULL,
                                            value TEXT NOT NULL,
                                            FOREIGN KEY (title_section_id) REFERENCES Title_Section (id)
                                        );"""

        sql_create_references_table = """CREATE TABLE IF NOT EXISTS Reference_Data (
                                        id INTEGER PRIMARY KEY,
                                        root_id INTEGER NOT NULL,
                                        FOREIGN KEY (root_id) REFERENCES Root (id)
                                    );"""

        sql_create_references_data = """CREATE TABLE IF NOT EXISTS Reference_Data_Items (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        reference_data_id INTEGER NOT NULL,
                                        key TEXT NOT NULL,
                                        value TEXT NOT NULL,
                                        FOREIGN KEY (reference_data_id) REFERENCES Reference_Data (id)
                                    );"""

        sql_create_first_inner_table = """CREATE TABLE IF NOT EXISTS First_Inner_Table (
                                        id INTEGER PRIMARY KEY,
                                        root_id INTEGER NOT NULL,
                                        FOREIGN KEY (root_id) REFERENCES Root (id)
                                    );"""

        sql_create_first_inner_title = """CREATE TABLE IF NOT EXISTS First_Inner_Title (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        first_inner_id INTEGER NOT NULL,
                                        value TEXT NOT NULL,
                                        FOREIGN KEY (first_inner_id) REFERENCES First_Inner_Table (id)
                                    );"""

        sql_create_manpower_table = """CREATE TABLE IF NOT EXISTS Manpower (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    first_inner_id INTEGER NOT NULL,
                                    category TEXT,
                                    level_type TEXT,
                                    quantity REAL,
                                    unit TEXT,
                                    rate_per_unit REAL,
                                    amount REAL,
                                    total_per_resource REAL,
                                    FOREIGN KEY (first_inner_id) REFERENCES First_Inner_Table (id)
                                );"""

        sql_create_materials_table = """CREATE TABLE IF NOT EXISTS Materials (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    first_inner_id INTEGER NOT NULL,
                                    category TEXT,
                                    level_type TEXT,
                                    quantity REAL,
                                    unit TEXT,
                                    rate_per_unit REAL,
                                    amount REAL,
                                    total_per_resource REAL,
                                    FOREIGN KEY (first_inner_id) REFERENCES First_Inner_Table (id)
                                );"""

        sql_create_machines_table = """CREATE TABLE IF NOT EXISTS Machines (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    first_inner_id INTEGER NOT NULL,
                                    category TEXT,
                                    level_type TEXT,
                                    quantity REAL,
                                    unit TEXT,
                                    rate_per_unit REAL,
                                    amount REAL,
                                    total_per_resource REAL,
                                    FOREIGN KEY (first_inner_id) REFERENCES First_Inner_Table (id)
                                );"""

        sql_create_others_table = """CREATE TABLE IF NOT EXISTS Others (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    first_inner_id INTEGER NOT NULL,
                                    category TEXT,
                                    level_type TEXT,
                                    quantity REAL,
                                    unit TEXT,
                                    rate_per_unit REAL,
                                    amount REAL,
                                    total_per_resource REAL,
                                    FOREIGN KEY (first_inner_id) REFERENCES First_Inner_Table (id)
                                );"""

        sql_create_second_inner_table = """CREATE TABLE IF NOT EXISTS Second_Inner_Table (
                                        id INTEGER PRIMARY KEY,
                                        root_id INTEGER NOT NULL,
                                        FOREIGN KEY (root_id) REFERENCES Root (id)
                                    );"""

        sql_create_second_inner_data = """CREATE TABLE IF NOT EXISTS Second_Inner_Data (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        second_inner_id INTEGER NOT NULL,
                                        key TEXT NOT NULL,
                                        value TEXT NOT NULL,
                                        FOREIGN KEY (second_inner_id) REFERENCES Second_Inner_Table (id)
                                    );"""

        try:
            c = conn.cursor()
            c.execute(sql_create_root_table)
            c.execute(sql_create_title_section_table)
            c.execute(sql_create_title_section_data)
            c.execute(sql_create_references_table)
            c.execute(sql_create_references_data)
            c.execute(sql_create_first_inner_table)
            c.execute(sql_create_first_inner_title)
            c.execute(sql_create_manpower_table)
            c.execute(sql_create_materials_table)
            c.execute(sql_create_machines_table)
            c.execute(sql_create_others_table)
            c.execute(sql_create_second_inner_table)
            c.execute(sql_create_second_inner_data)
        except Error as e:
            print(e)


    def insert_or_update_data(conn, data):
        """ Insert or update the hierarchical data in the database """

        for root_id, root_data in data.items():
            # Check if root exists
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Root WHERE id = ?", (root_id,))
            exists = cursor.fetchone()

            if exists:
                # Delete existing data for this root to avoid duplicates
                delete_root_data(conn, root_id)

            # Insert root
            conn.execute("INSERT INTO Root (id) VALUES (?)", (root_id,))

            # Insert Title_Section
            title_section = root_data.get('Title_Section', {})
            conn.execute("INSERT INTO Title_Section (id, root_id) VALUES (?, ?)",
                         (root_id, root_id))

            for key, values in title_section.items():
                for value in values:
                    if value:  # Only insert non-empty values
                        conn.execute("INSERT INTO Title_Section_Data (title_section_id, key, value) VALUES (?, ?, ?)",
                                     (root_id, key, value))

            # Insert Reference_Data
            references = root_data.get('References', {})
            conn.execute("INSERT INTO Reference_Data (id, root_id) VALUES (?, ?)",
                         (root_id, root_id))

            for key, values in references.items():
                for value in values:
                    if value or value == 0:  # Allow zero values
                        conn.execute("INSERT INTO Reference_Data_Items (reference_data_id, key, value) VALUES (?, ?, ?)",
                                     (root_id, key, str(value)))

            # Insert First Inner Table
            first_inner = root_data.get('First Inner table', {})
            conn.execute("INSERT INTO First_Inner_Table (id, root_id) VALUES (?, ?)",
                         (root_id, root_id))

            # Insert Title rows - only non-empty values
            for title_row in first_inner.get('Title', []):
                for value in title_row:
                    if value:  # Only insert non-empty values
                        conn.execute("INSERT INTO First_Inner_Title (first_inner_id, value) VALUES (?, ?)",
                                     (root_id, value))

            # Insert Manpower data
            for row in first_inner.get('Manpower', []):
                if row:  # Only insert if row exists
                    conn.execute("""INSERT INTO Manpower 
                                (first_inner_id, category, level_type, quantity, unit, rate_per_unit, amount, total_per_resource) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (root_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

            # Insert Materials data
            for row in first_inner.get('Materials', []):
                if row:  # Only insert if row exists
                    conn.execute("""INSERT INTO Materials 
                                (first_inner_id, category, level_type, quantity, unit, rate_per_unit, amount, total_per_resource) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (root_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

            # Insert Machines data
            for row in first_inner.get('Machines', []):
                if row:  # Only insert if row exists
                    conn.execute("""INSERT INTO Machines 
                                (first_inner_id, category, level_type, quantity, unit, rate_per_unit, amount, total_per_resource) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (root_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

            # Insert Others data
            for row in first_inner.get('Others', []):
                if row:  # Only insert if row exists
                    conn.execute("""INSERT INTO Others 
                                (first_inner_id, category, level_type, quantity, unit, rate_per_unit, amount, total_per_resource) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                 (root_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

            # Insert Second Inner Table
            second_inner = root_data.get('Second Inner table', {})
            conn.execute("INSERT INTO Second_Inner_Table (id, root_id) VALUES (?, ?)",
                         (root_id, root_id))

            for key, values in second_inner.items():
                for value in values:
                    if value or value == 0:  # Allow zero values
                        conn.execute("INSERT INTO Second_Inner_Data (second_inner_id, key, value) VALUES (?, ?, ?)",
                                     (root_id, key, str(value)))
        conn.commit()


    def delete_root_data(conn, root_id):
        """ Delete all data associated with a root_id """
        try:
            # Delete in reverse order of foreign key dependencies
            conn.execute(
                "DELETE FROM Second_Inner_Data WHERE second_inner_id IN (SELECT id FROM Second_Inner_Table WHERE root_id = ?)",
                (root_id,))
            conn.execute("DELETE FROM Second_Inner_Table WHERE root_id = ?", (root_id,))

            conn.execute(
                "DELETE FROM Manpower WHERE first_inner_id IN (SELECT id FROM First_Inner_Table WHERE root_id = ?)",
                (root_id,))
            conn.execute(
                "DELETE FROM Materials WHERE first_inner_id IN (SELECT id FROM First_Inner_Table WHERE root_id = ?)",
                (root_id,))
            conn.execute(
                "DELETE FROM Machines WHERE first_inner_id IN (SELECT id FROM First_Inner_Table WHERE root_id = ?)",
                (root_id,))
            conn.execute("DELETE FROM Others WHERE first_inner_id IN (SELECT id FROM First_Inner_Table WHERE root_id = ?)",
                         (root_id,))
            conn.execute(
                "DELETE FROM First_Inner_Title WHERE first_inner_id IN (SELECT id FROM First_Inner_Table WHERE root_id = ?)",
                (root_id,))
            conn.execute("DELETE FROM First_Inner_Table WHERE root_id = ?", (root_id,))

            conn.execute(
                "DELETE FROM Reference_Data_Items WHERE reference_data_id IN (SELECT id FROM Reference_Data WHERE root_id = ?)",
                (root_id,))
            conn.execute("DELETE FROM Reference_Data WHERE root_id = ?", (root_id,))

            conn.execute(
                "DELETE FROM Title_Section_Data WHERE title_section_id IN (SELECT id FROM Title_Section WHERE root_id = ?)",
                (root_id,))
            conn.execute("DELETE FROM Title_Section WHERE root_id = ?", (root_id,))

            conn.execute("DELETE FROM Root WHERE id = ?", (root_id,))
        except Error as e:
            print(f"Error deleting root data: {e}")


    def main():
        database = databasepath

        # Sample data (you provided)
        import InputData
        MappedData = InputData.mapped_Data

        # Create a database connection
        conn = create_connection(database)

        if conn is not None:
            # Create tables (will drop existing ones)
            create_tables(conn)

            # Insert data
            insert_or_update_data(conn, MappedData)

            # Close connection
            conn.close()
        else:
            print("Error! cannot create the database connection.")


    if __name__ == '__main__':
        main()





@dataclass
class SearchResult:
    root_id: int
    matched_field: str
    matched_value: str
    extracted_data: Dict[str, Any]
class SuperDataExtractor:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise ConnectionError(f"Database connection error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def smart_search(
            self,
            title_pattern: Optional[str] = None,
            content_pattern: Optional[str] = None,
            content_column: Optional[str] = None,
            extract_fields: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Flexible search across titles or table content
        Args:
            title_pattern: String to search in titles (None to skip title search)
            content_pattern: String to search in content (None to skip content search)
            content_column: Specific column to search in (None for any column)
            extract_fields: List of specific fields to extract ('Table_No', 'Overhead', etc.)
        Returns:
            List of SearchResult objects with matched data
        """
        results = []

        # Search by title if pattern provided
        if title_pattern:
            title_matches = self._search_titles(title_pattern)
            for match in title_matches:
                extracted = self._extract_specific_fields(match['root_id'], extract_fields)
                results.append(SearchResult(
                    root_id=match['root_id'],
                    matched_field='Title',
                    matched_value=match['title'],
                    extracted_data=extracted
                ))

        # Search by content if pattern provided
        if content_pattern:
            content_matches = self._search_content(content_pattern, content_column)
            for match in content_matches:
                # Avoid duplicates if same root_id matched by both title and content
                if not any(r.root_id == match['root_id'] for r in results):
                    extracted = self._extract_specific_fields(match['root_id'], extract_fields)
                    results.append(SearchResult(
                        root_id=match['root_id'],
                        matched_field=match['column'],
                        matched_value=match['matched_value'],
                        extracted_data=extracted
                    ))

        return results

    def _search_titles(self, pattern: str) -> List[Dict]:
        """Search for pattern in table titles"""
        query = """
            SELECT tsd.title_section_id as root_id, tsd.value as title
            FROM Title_Section_Data tsd
            WHERE tsd.key = 'Title' AND tsd.value LIKE ?
        """
        return self._execute_query(query, (f'%{pattern}%',))

    def _search_content(self, pattern: str, column: Optional[str] = None) -> List[Dict]:
        """
        Search for pattern in table content
        Searches: Manpower, Materials, Machines, Others tables
        """
        tables = ['Manpower', 'Materials', 'Machines', 'Others']
        results = []

        for table in tables:
            # Determine which columns to search
            if column:
                columns = [column]
            else:
                # Get all text columns for the table
                columns = self._get_text_columns(table)

            for col in columns:
                query = f"""
                    SELECT ft.root_id, ? as column, {col} as matched_value
                    FROM {table} t
                    JOIN First_Inner_Table ft ON t.first_inner_id = ft.id
                    WHERE {col} LIKE ?
                """
                matches = self._execute_query(query, (col, f'%{pattern}%'))
                results.extend(matches)

        return results

    def _get_text_columns(self, table: str) -> List[str]:
        """Get all text-type columns for a table"""
        # These are the text columns in our schema
        table_columns = {
            'Manpower': ['category', 'level_type', 'unit'],
            'Materials': ['category', 'level_type', 'unit'],
            'Machines': ['category', 'level_type', 'unit'],
            'Others': ['category', 'level_type', 'unit']
        }
        return table_columns.get(table, [])

    def _extract_specific_fields(self, root_id: int, fields: Optional[List[str]]) -> Dict[str, Any]:
        """Extract only requested fields from a table"""
        if not fields:
            return {}

        result = {}

        for field in fields:
            if field == 'Table_No':
                ref_data = self._execute_query("""
                    SELECT value FROM Reference_Data_Items
                    WHERE reference_data_id = ? AND key = 'Table No'
                """, (root_id,))
                if ref_data:
                    result['Table_No'] = ref_data[0]['value']

            elif field == 'Overhead':
                overhead_data = self._execute_query("""
                    SELECT value FROM Second_Inner_Data
                    WHERE second_inner_id = ? AND key = 'Overhead'
                """, (root_id,))
                if overhead_data:
                    result['Overhead'] = self._convert_value(overhead_data[0]['value'])

            elif field == 'Title':
                title_data = self._execute_query("""
                    SELECT value FROM Title_Section_Data
                    WHERE title_section_id = ? AND key = 'Title'
                """, (root_id,))
                if title_data:
                    result['Title'] = title_data[0]['value']

            # Add more field extractors as needed

        return result

    def _execute_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute query with parameters and return results as dicts"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise ValueError(f"Query execution error: {e}")

    def _convert_value(self, value: str) -> Union[int, float, str]:
        """Convert string values to appropriate Python types"""
        if value is None:
            return None
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value

    def search_resources(
            self,
            resource_type: str,  # 'all', 'labour', 'materials', 'machines'
            search_column: str,  # Column name to search in
            search_value: str,  # Value to search for
            exact_match: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search across specified resource types and return matching tables
        Args:
            resource_type: Type of resource to search
            search_column: Column name to search in
            search_value: Value to search for
            exact_match: Whether to require exact match
        Returns:
            List of matching tables with basic info
        """
        # Map resource types to tables
        resource_tables = {
            'labour': ['Manpower'],
            'materials': ['Materials'],
            'machines': ['Machines'],
            'all': ['Manpower', 'Materials', 'Machines', 'Others']
        }.get(resource_type.lower(), [])

        if not resource_tables:
            raise ValueError("Invalid resource type. Use 'labour', 'materials', 'machines' or 'all'")

        results = []
        search_pattern = search_value if exact_match else f'%{search_value}%'

        for table in resource_tables:
            query = f"""
                SELECT 
                    fit.root_id,
                    t.{search_column} as matched_value,
                    tsd.value as title
                FROM {table} t
                JOIN First_Inner_Table fit ON t.first_inner_id = fit.id
                JOIN Title_Section ts ON fit.root_id = ts.root_id
                JOIN Title_Section_Data tsd ON ts.id = tsd.title_section_id AND tsd.key = 'Title'
                WHERE t.{search_column} LIKE ?
            """
            matches = self._execute_query(query, (search_pattern,))
            results.extend([{
                'table_type': table,
                'root_id': row['root_id'],
                'matched_column': search_column,
                'matched_value': row['matched_value'],
                'title': row['title']
            } for row in matches])

        return results

    def get_table_data(
            self,
            root_id: int,
            data_type: str = 'all'  # 'all', 'basic', 'overhead', 'rates', 'references'
    ) -> Dict[str, Any]:
        """
        Get comprehensive data for a specific table
        Args:
            root_id: The root ID of the table
            data_type: Type of data to retrieve
        Returns:
            Dictionary with requested data
        """
        result = {}

        # Always include basic info
        if data_type in ['all', 'basic']:
            result['basic'] = {
                'title': self._get_title_section(root_id).get('Title', [''])[0],
                'references': self._get_references(root_id)
            }

        # Include first inner table data
        if data_type in ['all', 'basic', 'rates']:
            first_inner = self._get_first_inner_table(root_id)
            result['resources'] = {
                'manpower': first_inner.get('Manpower', []),
                'materials': first_inner.get('Materials', []),
                'machines': first_inner.get('Machines', [])
            }

        # Include second inner table data
        if data_type in ['all', 'overhead']:
            second_inner = self._get_second_inner_table(root_id)
            result['costs'] = {
                'overhead': second_inner.get('Overhead', []),
                'rates': second_inner.get('Unit Rate', [])
            }

        return result
    def _get_title_section(self, root_id: int) -> Dict[str, List]:
        """Get title section data for a specific root ID"""
        query = """
            SELECT key, value FROM Title_Section_Data
            WHERE title_section_id = ?
        """
        data = {}
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (root_id,))
            for key, value in cursor.fetchall():
                if key not in data:
                    data[key] = []
                data[key].append(value)
        except sqlite3.Error as e:
            print(f"Error getting title section: {e}")
        return data

    def _get_references(self, root_id: int) -> Dict[str, List]:
        """Get references data for a specific root ID"""
        query = """
            SELECT key, value FROM Reference_Data_Items
            WHERE reference_data_id = ?
        """
        data = {}
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (root_id,))
            for key, value in cursor.fetchall():
                if key not in data:
                    data[key] = []
                # Try to convert numeric values
                try:
                    data[key].append(float(value) if '.' in value else int(value))
                except ValueError:
                    data[key].append(value)
        except sqlite3.Error as e:
            print(f"Error getting references: {e}")
        return data

    def _get_first_inner_table(self, root_id: int) -> Dict[str, List]:
        """Get first inner table data for a specific root ID"""
        data = {
            'Title': self._get_inner_title(root_id),
            'Manpower': self._get_inner_data('Manpower', root_id),
            'Materials': self._get_inner_data('Materials', root_id),
            'Machines': self._get_inner_data('Machines', root_id),
            'Others': self._get_inner_data('Others', root_id)
        }
        return data

    def _get_second_inner_table(self, root_id: int) -> Dict[str, List]:
        """Get second inner table data for a specific root ID"""
        query = """
            SELECT key, value FROM Second_Inner_Data
            WHERE second_inner_id = ?
        """
        data = {}
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (root_id,))
            for key, value in cursor.fetchall():
                if key not in data:
                    data[key] = []
                # Try to convert numeric values
                try:
                    data[key].append(float(value) if '.' in value else int(value))
                except ValueError:
                    data[key].append(value)
        except sqlite3.Error as e:
            print(f"Error getting second inner table: {e}")
        return data

    def _get_inner_title(self, root_id: int) -> List[List[str]]:
        """Get inner table title rows"""
        query = """
            SELECT value FROM First_Inner_Title
            WHERE first_inner_id = ?
            ORDER BY id
        """
        titles = []
        current_row = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (root_id,))
            for (value,) in cursor.fetchall():
                current_row.append(value)
                if len(current_row) >= 7:  # Assuming 7 columns per row
                    titles.append(current_row)
                    current_row = []
            if current_row:  # Add any remaining items
                titles.append(current_row)
        except sqlite3.Error as e:
            print(f"Error getting inner title: {e}")
        return titles

    def _get_inner_data(self, table: str, root_id: int) -> List[List]:
        """Get data from specific inner table"""
        query = f"""
            SELECT * FROM {table}
            WHERE first_inner_id = ?
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (root_id,))
            return [list(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error getting {table} data: {e}")
            return []

    def find_tables(
            self,
            search_criteria: Dict[str, Any],
            max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Find tables matching multiple search criteria
        Args:
            search_criteria: {
                'search_type': 'title'|'resource',
                # For title search:
                'title_pattern': str,
                'exact_match': bool (default False),
                # For resource search:
                'resource_type': 'labour'|'materials'|'machines'|'all' (required for resource search),
                'search_column': str (required for resource search),
                'search_value': str (required for resource search)
            }
            max_results: optional limit on number of results
        Returns:
            List of matching tables with basic info
        """
        search_type = search_criteria.get('search_type')

        if search_type == 'title':
            # Handle title search
            if 'title_pattern' not in search_criteria:
                raise ValueError("title_pattern is required for title search")
            return self.find_tables_by_title(
                title_pattern=search_criteria['title_pattern'],
                exact_match=search_criteria.get('exact_match', False),
                max_results=max_results
            )
        elif search_type == 'resource':
            # Handle resource search
            required = ['search_column', 'search_value']  # Removed resource_type from required
            for field in required:
                if field not in search_criteria:
                    raise ValueError(f"{field} is required for resource search")

            # Default to searching all resource types if not specified
            resource_type = search_criteria.get('resource_type', 'all')

            return self.search_resources(
                resource_type=resource_type,
                search_column=search_criteria['search_column'],
                search_value=search_criteria['search_value'],
                exact_match=search_criteria.get('exact_match', False)
            )
        # elif search_type == 'resource':
        #     # Handle resource search
        #     required = ['resource_type', 'search_column', 'search_value']
        #     for field in required:
        #         if field not in search_criteria:
        #             raise ValueError(f"{field} is required for resource search")
        #     return self.search_resources(
        #         resource_type=search_criteria['resource_type'],
        #         search_column=search_criteria['search_column'],
        #         search_value=search_criteria['search_value'],
        #         exact_match=search_criteria.get('exact_match', False)
        #     )
        else:
            raise ValueError("Invalid search_type. Use 'title' or 'resource'")

    def extract_table_contents(
            self,
            table_ids: List[int],
            content_types: List[str] = ['basic', 'resources', 'costs']
    ) -> Dict[int, Dict[str, Any]]:
        """
        Extract specified content from multiple tables
        Args:
            table_ids: List of root_ids to extract
            content_types: Types of data to extract
        Returns:
            Dictionary with root_id as key and extracted data as value
        """
        results = {}

        for table_id in table_ids:
            table_data = {}

            if 'basic' in content_types:
                table_data['basic'] = {
                    'title': self._get_title_section(table_id).get('Title', [''])[0],
                    'references': self._get_references(table_id)
                }

            if 'resources' in content_types:
                first_inner = self._get_first_inner_table(table_id)
                table_data['resources'] = {
                    'manpower': first_inner.get('Manpower', []),
                    'materials': first_inner.get('Materials', []),
                    'machines': first_inner.get('Machines', [])
                }

            if 'costs' in content_types:
                second_inner = self._get_second_inner_table(table_id)
                table_data['costs'] = {
                    'overhead': second_inner.get('Overhead', []),
                    'rates': second_inner.get('Unit Rate', [])
                }

            results[table_id] = table_data

        return results

    def find_tables_by_title(
            self,
            title_pattern: str,
            exact_match: bool = False,
            max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Find tables matching title pattern
        Args:
            title_pattern: String to search in titles
            exact_match: Whether to require exact match
            max_results: Optional limit on number of results
        Returns:
            List of matching tables with basic info
        """
        query = """
            SELECT 
                tsd.title_section_id as root_id,
                tsd.value as title
            FROM Title_Section_Data tsd
            WHERE tsd.key = 'Title'
        """

        if exact_match:
            query += " AND tsd.value = ?"
            params = (title_pattern,)
        else:
            query += " AND tsd.value LIKE ?"
            params = (f'%{title_pattern}%',)

        if max_results is not None:
            query += f" LIMIT {max_results}"

        return self._execute_query(query, params)

# Usage Examples
databasepath = "DUDBC_RateAnalysis.db"
# DUDBC_RateWriter(databasepath)

def DUDBC_Extractor(searchmode, searchvalue, resourcetype = ""):
    search_criteria= {}
    if searchmode == "title":
        search_criteria = {
            # # Title search example:
            'search_type': searchmode,
            'title_pattern': searchvalue,
            'exact_match': False
        }

    if searchmode == "resource":
        search_criteria = {
            'search_type': searchmode,
            'search_column': 'level_type',
            'resource_type': resourcetype,  # Optional - will search all types if omitted
            'search_value': searchvalue

        }

    db_path = "DUDBC_RateAnalysis.db"

    with SuperDataExtractor(db_path) as extractor:
        # Perform the search
        matched_tables = extractor.find_tables(search_criteria)
        all_tables_data = {}

        if not matched_tables:
            print("No matching tables found")
        else:
            # Dictionary to store all tables in the requested format
            all_tables_data = {}

            for table in matched_tables:
                table_id = table['root_id']

                # Get all data for this table
                full_data = {
                    'Title_Section': {},
                    'References': {},
                    'First Inner table': {
                        'Title': [],
                        'Manpower': [],
                        'Materials': [],
                        'Machines': [],
                        'Others': []
                    },
                    'Second Inner table': {}
                }

                # 1. Get Title Section
                title_data = extractor._get_title_section(table_id)
                full_data['Title_Section'] = title_data

                # 2. Get References
                ref_data = extractor._get_references(table_id)
                full_data['References'] = ref_data

                # 3. Get First Inner Table
                first_inner = extractor._get_first_inner_table(table_id)
                def indexContente_splitter(list, title):
                    Contents = []
                    Indexes = []
                    for table in list:
                        Contents.append(table[2:])
                        Indexes.append(table[0:2])

                    full_data['First Inner table'][title] = Contents

                indexContente_splitter(first_inner['Manpower'], "Manpower")
                indexContente_splitter(first_inner['Materials'], "Materials")
                indexContente_splitter(first_inner['Machines'], "Machines")
                full_data['First Inner table']['Others'] = first_inner['Others']



                # 4. Get Second Inner Table
                second_inner = extractor._get_second_inner_table(table_id)
                full_data['Second Inner table'] = second_inner

                # Add to our complete collection
                all_tables_data[table_id] = full_data

            # Print the first table's data in the exact requested format
            # print(all_tables_data)
            TableKeys = list(all_tables_data.keys())
            # for table_id in TableKeys:
            #     print(f"{table_id}: {all_tables_data[table_id]}")
                ### printsample = 187: {'Title_Section': {'Title': ['नयाँ सर्फेसमा ह्वाईटवास दुईकोट गर्ने काम (सिलिंगमा)'], 'Note': ['दर विश्लेषणको लागि १०० व.मी. लिइएको']}, 'References': {'Table No': [192], 'Reference': ['J 1']}, 'First Inner table': {'Title': [], 'Manpower': [['श्रमिक', 'क) सिपालु', 1.875, 'जवान', 1190.0, 2231.25, None], ['श्रमिक', 'ख) ज्यामी', 1.375, 'जवान', 863.0, 1186.6200000000001, 3417.87]], 'Materials': [['निर्माण सामग्री', 'सेतो चुना', 22.0, 'के.जी.', 21.25, 467.5, None], ['निर्माण सामग्री', 'गम आदि', 0.88, 'के.जी.', 290.7, 255.81, 723.31]], 'Machines': [], 'Others': []}, 'Second Inner table': {'Original Rate': [4141.18], 'Overhead': [621.17], 'Total Rate': [4762.35], 'Unit Rate': [47.62], 'Others': ['दर प्रति व.मी.को', 4762.35, 100]}}


            with open('all_tables_data.json', 'w', encoding='utf-8') as f:
                json.dump(all_tables_data, f, indent=2, ensure_ascii=False)
        return all_tables_data



# DUDBC_Extractor("title", " सिमेन्ट पेन्ट", resourcetype = "")
# ####'labour', 'materials', 'machines' or 'all'
# DUDBC_Extractor("resource", "डिस्टेम्पर पाउडर", resourcetype = "all")

#Results
# 194: {'Title_Section': {'Title': ['वाटर प्रुफ सिमेन्ट पेन्ट एक कोट लगाउने काम ।'], 'Note': ['दर विश्लेषणको लागि १०० व.मी. लिइएको']}, 'References': {'Table No': [199], 'Reference': ['J 4']}, 'First Inner table': {'Title': [], 'Manpower': [['श्रमिक', 'क) सिपालु', 1.7, 'जवान', 1190.0, 2023.0, None], ['श्रमिक', 'ख) ज्यामी', 1.7, 'जवान', 863.0, 1467.1000000000001, 3490.1000000000004]], 'Materials': [['निर्माण सामग्री', 'सिमेन्ट पेन्ट', 30.0, 'के.जी.', 42.84, 1285.2, 1285.2], ['निर्माण सामग्री', None, None, None, None, None, None]], 'Machines': [], 'Others': []}, 'Second Inner table': {'Original Rate': [4775.3], 'Overhead': [716.29], 'Total Rate': [5491.59], 'Unit Rate': [54.91], 'Others': ['दर प्रति व.मी.को', 5491.59, 100]}}
# 195: {'Title_Section': {'Title': ['वाटर प्रुफ सिमेन्ट पेन्ट दुई कोट लगाउने काम ।'], 'Note': ['दर विश्लेषणको लागि १०० व.मी. लिइएको']}, 'References': {'Table No': [200], 'Reference': ['J 4']}, 'First Inner table': {'Title': [], 'Manpower': [['श्रमिक', 'क) सिपालु', 5.0, 'जवान', 1190.0, 5950.0, None], ['श्रमिक', 'ख) ज्यामी', 5.0, 'जवान', 863.0, 4315.0, 10265.0]], 'Materials': [['निर्माण सामग्री', 'सिमेन्ट पेन्ट', 48.5, 'के.जी.', 42.84, 2077.7400000000002, 2077.7400000000002], ['निर्माण सामग्री', None, None, None, None, None, None]], 'Machines': [], 'Others': []}, 'Second Inner table': {'Original Rate': [12342.74], 'Overhead': [1851.41], 'Total Rate': [14194.15], 'Unit Rate': [141.94], 'Others': ['दर प्रति व.मी.को', 14194.15, 100]}}
# 192: {'Title_Section': {'Title': ['डिस्टेम्पर लगाउने काम एक कोट ।'], 'Note': ['दर विश्लेषणको लागि १०० व.मी. लिइएको']}, 'References': {'Table No': [197], 'Reference': ['J 3']}, 'First Inner table': {'Title': [], 'Manpower': [['श्रमिक', 'क) सिपालु', 4.0, 'जवान', 1190.0, 4760.0, None], ['श्रमिक', 'ख) ज्यामी', 4.0, 'जवान', 863.0, 3452.0, 8212.0]], 'Materials': [['निर्माण सामग्री', 'अस्तर', 8.0, 'ली.', 397.8, 3182.4, None], ['निर्माण सामग्री', 'डिस्टेम्पर पाउडर', 6.5, 'के.जी.', 163.2, 1060.8, 4243.2]], 'Machines': [], 'Others': []}, 'Second Inner table': {'Original Rate': [12455.2], 'Overhead': [1868.28], 'Total Rate': [14323.480000000001], 'Unit Rate': [143.23], 'Others': ['दर प्रति व.मी.को', 14323.480000000001, 100]}}
# 193: {'Title_Section': {'Title': ['डिस्टेम्पर लगाउने काम दुई कोट ।'], 'Note': ['दर विश्लेषणको लागि १०० व.मी. लिइएको']}, 'References': {'Table No': [198], 'Reference': ['J 3']}, 'First Inner table': {'Title': [], 'Manpower': [['श्रमिक', 'क) सिपालु', 5.8, 'जवान', 1190.0, 6902.0, None], ['श्रमिक', 'ख) ज्यामी', 5.8, 'जवान', 863.0, 5005.400000000001, 11907.400000000001]], 'Materials': [['निर्माण सामग्री', 'अस्तर', 8.0, 'ली.', 397.8, 3182.4, None], ['निर्माण सामग्री', 'डिस्टेम्पर पाउडर', 11.5, 'के.जी.', 163.2, 1876.8, 5059.2]], 'Machines': [], 'Others': []}, 'Second Inner table': {'Original Rate': [16966.600000000002], 'Overhead': [2544.9900000000002], 'Total Rate': [19511.590000000004], 'Unit Rate': [195.11], 'Others': ['दर प्रति व.मी.को', 19511.590000000004, 100]}}








#DatabaseWrite

class GUIDatabase:
    def __init__(self, db_name="estimation.db"):
        if os.path.exists(db_name):
            os.remove(db_name)

        # Create a fresh database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # General Info table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS General_Info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            office TEXT,
            projectname TEXT,
            officeCode TEXT,
            projectlocation TEXT,
            projectcompletiontime TEXT,
            fiscalyear TEXT,
            budgetsubheadingno TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS quantity_estimation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            EstimationPartSection_root TEXT,
            estimation_Section_title TEXT,
            items_section_Title TEXT,
            dropdown TEXT,
            search_keyword_input TEXT,
            search_button TEXT,
            dynamic_saerchResults_container TEXT,
            item_number TEXT,
            item_description TEXT,
            unit TEXT,
            rate REAL,
            numbers REAL,
            length REAL,
            breadth REAL,
            height REAL,
            quantity REAL,
            remarks TEXT,
            calc_info TEXT,
            quantity_factor REAL,
            Item_cost REAL
        )
        """)



        # Search Results (applied items)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Rate_Analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_number TEXT NOT NULL,
            norms_ref TEXT,
            section TEXT,
            attribute TEXT,
            value TEXT,
            resource_type TEXT,
            category TEXT,
            quantity REAL,
            unit TEXT,
            rate REAL,
            amount REAL,
            amount_perHeading REAL
        )
        """)
        self.conn.commit()
    def save_GenInfo_QEstimation(self, ObjectsCache):
        def get_text(obj):
            try:
                return str(obj.text)
            except Exception:
                return str(obj)  # fallback if no .text attr

        def safe_float(val, default=0.0):
            try:
                return float(val)
            except (ValueError, TypeError):
                return default

        # --- Save General Information ---
        general_info = ObjectsCache["Estimation_Data"]["General_Information"]

        general_values = (
            get_text(general_info["office"]),
            get_text(general_info["projectname"]),
            get_text(general_info["officeCode"]),
            get_text(general_info["projectlocation"]),
            get_text(general_info["projectcompletiontime"]),
            get_text(general_info["fiscalyear"]),
            get_text(general_info["budgetsubheadingno"]),
        )

        # Clear existing rows and insert fresh one
        self.cursor.execute("DELETE FROM General_Info")
        self.cursor.execute("""
            INSERT INTO General_Info (
                office, projectname, officeCode, projectlocation,
                projectcompletiontime, fiscalyear, budgetsubheadingno
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, general_values)

        # --- Save Quantity Estimation ---
        sections = ObjectsCache["Estimation_Data"]["Estimation_Sections"]

        for _, section in sections.items():
            item_number = get_text(section["item_number"])

            values = (
                str(section["EstimationPartSection_root"]),
                get_text(section["estimation_Section_title"]),
                get_text(section["items_section_Title"]),
                get_text(section["dropdown"]),
                get_text(section["search_keyword_input"]),
                get_text(section["search_button"]),
                get_text(section["dynamic_saerchResults_container"]),
                item_number,
                get_text(section["item_description"]),
                get_text(section["unit"]),
                safe_float(get_text(section["rate"])),
                safe_float(get_text(section["numbers"])),
                safe_float(get_text(section["length"])),
                safe_float(get_text(section["breadth"])),
                safe_float(get_text(section["height"])),
                safe_float(get_text(section["quantity"])),
                get_text(section["remarks"]),
                str(section["calc_info"]),
                safe_float(get_text(section["quantity_factor"])),
                safe_float(get_text(section["Item_cost"])),
            )
            # print(values)

            # Check if row exists with same item_number
            self.cursor.execute("SELECT id FROM quantity_estimation WHERE item_number = ?", (item_number,))
            existing = self.cursor.fetchone()

            if existing:
                # Delete old row
                self.cursor.execute("DELETE FROM quantity_estimation WHERE item_number = ?", (item_number,))

            # Insert new/updated row
            self.cursor.execute("""
                INSERT INTO quantity_estimation (
                    EstimationPartSection_root, estimation_Section_title,
                    items_section_Title, dropdown, search_keyword_input, search_button,
                    dynamic_saerchResults_container, item_number, item_description,
                    unit, rate, numbers, length, breadth, height, quantity,
                    remarks, calc_info, quantity_factor, Item_cost
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)

        self.conn.commit()
    def close(self):
        self.conn.close()



#_________________-Check below

    def save_appliedRateAnalysis(self, item_number, appliedRateData):
        conn = sqlite3.connect("estimation.db")
        c = conn.cursor()

        # First remove all rows with this item_number
        c.execute("DELETE FROM Rate_Analysis WHERE item_number = ?", (item_number,))

        # ---- Title_Section ----
        for k, v in appliedRateData.get("Title_Section", {}).items():
            for entry in v:
                c.execute("""
                    INSERT INTO Rate_Analysis (item_number, norms_ref, section, attribute, value)
                    VALUES (?, ?, ?, ?, ?)
                """, (item_number, appliedRateData.get("NormsDBRef", ""), "Title_Section", k, str(entry)))

        # ---- References ----
        for k, v in appliedRateData.get("References", {}).items():
            for entry in v:
                c.execute("""
                    INSERT INTO Rate_Analysis (item_number, norms_ref, section, attribute, value)
                    VALUES (?, ?, ?, ?, ?)
                """, (item_number, appliedRateData.get("NormsDBRef", ""), "References", k, str(entry)))

        # ---- First Inner Table ----
        inner = appliedRateData.get("First Inner table", {})

        def insert_resource(rows, resource_type):
            for row in rows:
                c.execute("""
                    INSERT INTO Rate_Analysis (
                        item_number, norms_ref, section, attribute,
                        resource_type, category, quantity, unit, rate, amount, amount_perHeading
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item_number, appliedRateData.get("NormsDBRef", ""),
                    "First Inner table", resource_type,
                    row[0], row[1], row[2], row[3], row[4], row[5],
                    row[6] if len(row) > 6 else None  # 7th item stored in extra
                ))

        insert_resource(inner.get("Manpower", []), "Manpower")
        insert_resource(inner.get("Materials", []), "Materials")
        insert_resource(inner.get("Machines", []), "Machines")

        # ---- Second Inner Table ----
        for k, v in appliedRateData.get("Second Inner table", {}).items():
            for entry in v:
                c.execute("""
                    INSERT INTO Rate_Analysis (item_number, norms_ref, section, attribute, value)
                    VALUES (?, ?, ?, ?, ?)
                """, (item_number, appliedRateData.get("NormsDBRef", ""), "Second Inner table", k, str(entry)))

        conn.commit()
    def load_appliedRateAnalysis(self, item_number=None, norms_ref=None):
        """
        Extract data from Rate_Analysis table and reconstruct appliedRateData
        in the exact format it was saved.

        Parameters:
            item_number (str): specific item_number to filter.
            norms_ref (str/int): specific NormsDBRef to filter.

        Returns:
            appliedRateData (dict)
        """
        conn = sqlite3.connect("estimation.db")
        c = conn.cursor()

        # Initialize the structure
        appliedRateData = {
            "NormsDBRef": "",
            "Title_Section": {},
            "References": {},
            "First Inner table": {
                "Title": [["स्रोत साधन", "तह/किसिम", "परिमाण", "एकाई", "दर प्रति एकाई", "रकम",
                           "प्रत्येक स्रोत साधनको जम्मा"]],
                "Manpower": [],
                "Materials": [],
                "Machines": [],
                "Others": []
            },
            "Second Inner table": {}
        }

        # Build query based on filters
        conn = sqlite3.connect("estimation.db")
        c = conn.cursor()

        # Base query
        query = "SELECT * FROM Rate_Analysis WHERE 1=1"
        params = []

        # Filter by item_number if provided
        if item_number is not None:
            query += " AND item_number=?"
            params.append(item_number)

        # Filter by norms_ref if provided
        if norms_ref is not None:
            query += " AND norms_ref=?"
            params.append(norms_ref)

        # Execute query
        c.execute(query, params)
        rows = c.fetchall()

        if not rows:
            conn.close()
            return rows,  appliedRateData

        # Get column names
        col_names = [desc[0] for desc in c.description]

        # Fetch NormsDBRef from first non-empty row
        for row in rows:
            idx = col_names.index("norms_ref")
            if row[idx]:
                appliedRateData["NormsDBRef"] = row[idx]
                break

        # Process each row
        for row in rows:
            section = row[col_names.index("section")]
            attribute = row[col_names.index("attribute")]

            if section == "Title_Section":
                value = row[col_names.index("value")]
                if attribute not in appliedRateData["Title_Section"]:
                    appliedRateData["Title_Section"][attribute] = []
                appliedRateData["Title_Section"][attribute].append(value)

            elif section == "References":
                value = row[col_names.index("value")]
                if attribute not in appliedRateData["References"]:
                    appliedRateData["References"][attribute] = []
                appliedRateData["References"][attribute].append(value)

            elif section == "First Inner table":
                resource_type = row[col_names.index("attribute")]
                entry = [
                    row[col_names.index("resource_type")],
                    row[col_names.index("category")],
                    row[col_names.index("quantity")],
                    row[col_names.index("unit")],
                    row[col_names.index("rate")],
                    row[col_names.index("amount")],
                    row[col_names.index("amount_perHeading")]
                ]
                if resource_type in ["Manpower", "Materials", "Machines"]:
                    appliedRateData["First Inner table"][resource_type].append(entry)
                else:
                    appliedRateData["First Inner table"]["Others"].append(entry)

            elif section == "Second Inner table":
                value = row[col_names.index("value")]
                if attribute not in appliedRateData["Second Inner table"]:
                    appliedRateData["Second Inner table"][attribute] = []
                appliedRateData["Second Inner table"][attribute].append(value)

        conn.close()
        return rows, appliedRateData

    def ResetRate_QunatityEstimation(self):
        conn = sqlite3.connect("estimation.db")
        c = conn.cursor()

        #Deletes the whole quantity_estimation table
        c.execute("DELETE FROM quantity_estimation")  # remove all rows
        c.execute("DELETE FROM sqlite_sequence WHERE name='quantity_estimation'")  # reset autoincrement
        conn.commit()

        #Deletes the whole quantity_estimation table
        c.execute("DELETE FROM Rate_Analysis")  # remove all rows
        c.execute("DELETE FROM sqlite_sequence WHERE name='Rate_Analysis'")  # reset autoincrement
        conn.commit()

        conn.close()


    def delete_SubItemData_(self, item_number):
        conn = sqlite3.connect("estimation.db")
        c = conn.cursor()

        c.execute("SELECT id FROM quantity_estimation WHERE item_number = ?", (item_number,))
        existing = c.fetchone()
        # print("_____________________________________________________________")
        # print(existing, "existing", item_number)

        if existing:
            c.execute("DELETE FROM quantity_estimation WHERE item_number = ?", (item_number,))
            conn.commit()

        c.execute("SELECT id FROM quantity_estimation WHERE item_number = ?", (item_number,))
        existing = c.fetchone()
        # print(existing, "existing")
        conn.close()
