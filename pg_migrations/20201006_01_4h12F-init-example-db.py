"""
init example db
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table posts (
                id serial,
                title varchar(100),
                content varchar(500),
                additional_data json
            );
            
            create table features (
                id serial,
                is_active bool,
                feature_name varchar(20)
            );
            
            insert into posts (title, content, additional_data) values 
                ('test 1', 'test content 1', '{"test": "data 1"}'),
                ('test 2', 'test content 2', '{"test": "data 2"}'),
                ('test 3', 'test content 3', '{"test": "data 3"}'),
                ('test 4', 'test content 4', '{"test": "data 4"}'),
                ('test 5', 'test content 5', '{"test": "data 5"}'),
                ('test 6', 'test content 6', '{"test": "data 6"}');
            
            insert into features (is_active, feature_name) values 
                (true, 'active feature'),
                (true, 'active feature2'),
                (false, 'disabled feature'),
                (true, 'active feature3');
            
        """
    )
]
