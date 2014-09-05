
class Activity:

    get_objective_id_template = """
        # Implemented from template for osid.learning.Activity.get_objective_id
        try:
            from ..id.primitives import Id
        except:
            from ..osid.common import Id
        return Id(self.my_model.${var_name}_authority,
                  self.my_model.${var_name}_namespace,
                  self.my_model.${var_name}_identifier)"""

    get_objective_template = """
        # Implemented from template for osid.learning.Activity.get_objective_id
        from .osid_errors import OperationFailed
        try:
            from ..${return_app_name}.${return_djpkg_name} import managers
        except ImportError:
            raise OperationFailed('failed to import ${return_app_name}.${return_djpkg_name}.managers')
${import_str}        try:
            mgr = managers.${return_pkg_title}Manager()
        except:
            raise OperationFailed('failed to instantiate ${return_pkg_title}Manager')
        if not mgr.supports_${return_type_under}_lookup():
            raise OperationFailed('${return_pkg_title} does not support ${return_type} lookup')
        try:
            osid_object = mgr.get_${return_type_under}_lookup_session().get${return_type_under}(self.get_${var_name}_id())
        except:
            raise OperationFailed()
        else:
            return osid_object"""

    is_asset_based_activity_template = """
        # Implemented from template for osid.learning.Activity.is_asset_based_activity_template
        return self.my_model.${var_name}"""

    get_asset_ids = """
        pass # IMPLEMENT ME NEXT!"""

    get_assets = """
        pass # IMPLEMENT ME NEXT!"""


