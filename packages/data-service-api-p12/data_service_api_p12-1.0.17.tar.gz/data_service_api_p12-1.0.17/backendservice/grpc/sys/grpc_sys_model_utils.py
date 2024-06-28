from backendservice.grpc.grpcutils import value_or_empty, bytes_or_empty
from backendservice.grpc.sys.sysservice_pb2 import TokenUser_
from backendservice.util.utils import get_dict_val, is_not_blank


class TokenUser2:

    def __init__(self, exp=0, name="", user_id="" , roles=""):
        self.exp =  exp
        self.name = name
        self.user_id =user_id
        self.roles = roles

    def __str__(self):
        return f"user:{self.name}, uid:{self.user_id},roles:{self.roles},exp:{self.exp}"



class pb2_to_local:
    """

    # 将 GRPC 数据转换为 Python Models

    """

    @staticmethod
    def to_TokenUser2 (user: TokenUser_) -> TokenUser2 :
        exp = user.exp
        sub = user.sub
        uid = user.uid
        roles = user.roles

        out = TokenUser2(exp, sub, uid, roles )
        return out



#####################################################################################################################


class local_to_pb2:
    """

    # 将 Python Models  数据转换为 GRPC

    """


    @staticmethod
    def to_TokenUser_(user: TokenUser2) -> TokenUser_:
        exp = user.exp
        sub = user.name
        uid = user.user_id
        roles = user.roles

        out = TokenUser_(exp= exp, sub=value_or_empty(sub), uid=value_or_empty(uid), roles=value_or_empty(roles ) )
        return out