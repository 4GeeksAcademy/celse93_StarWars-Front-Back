from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField
from sqlalchemy.orm import RelationshipProperty


class StandardModelView(ModelView):
    column_display_pk = True
    column_display_all_relations = True

    def scaffold_form(self):
        form_class = super().scaffold_form()

        # Remove all "list" relationships from the form
        for attr_name, attr in self.model.__mapper__.all_orm_descriptors.items():
            if isinstance(getattr(self.model, attr_name).property, RelationshipProperty):
                prop = getattr(self.model, attr_name).property
                if prop.uselist:
                    if attr_name in form_class.__dict__:
                        delattr(form_class, attr_name)

        # Replace foreign key integer fields with SelectField using the relationship
        for column in self.model.__table__.columns:
            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                rel = None
                for rel_name, rel_prop in self.model.__mapper__.relationships.items():
                    if fk.column.table == rel_prop.mapper.local_table:
                        rel = rel_prop
                        break
                if not rel:
                    continue

                related_class = rel.mapper.class_
                choices = [(str(obj.id), str(obj))
                           for obj in self.session.query(related_class).all()]

                if column.name in form_class.__dict__:
                    setattr(form_class, column.name, SelectField(
                        column.name, choices=choices))

        return form_class
