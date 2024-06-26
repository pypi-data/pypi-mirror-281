"""
Node objects definition

There are two main types of node objects`, noth of which are subclasses
of the `_BaseNode` class:
- `Node` should be used for defining all documented taxonomic nodes.
- `DummyNode`can be used to add non-existing nodes, for example
  at missing ranks in order to normalize different branches

In addition, the `MergedNode` class serves to create references to
another `Node` for taxomic IDs that no longer exist due to being merged
with other IDs.
"""


from __future__ import annotations
from typing import Union, Optional
from .utils import _rand_id


class _BaseNode:
    """
    Base object for Node classes

    This is meant for internal use. Nodes should be instanciated from
    a subclass of `_BaseNode`, preferably `Node`.

    Parameters
    ---------
    taxid: str or int
        Taxonomic identification number
    name: str, optional
        Node name
    rank: str, optional
        Node rank
    parent: _BaseNode, optional
        The parent Node object

    Notes
    -----
    The `children` property will be dynamically populated when children Nodes
    declare a Node as parent.

    Attributes
    ----------
    taxid
    name
    rank
    children
    parent
    node_info
    """
    def __init__(self,
                 taxid: Union[str, int] = None,
                 name: Optional[str] = None,
                 rank: Optional[str] = None,
                 parent: Optional[_BaseNode] = None
                ) -> None:
        self._children = set()
        self._name = name
        self._rank = rank
        self._parent = parent
        self._taxid = str(taxid) if taxid != None else taxid

        self._updateParent()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.taxid})"

    # Property methods
    @property
    def taxid(self) -> str:
        """Taxonomic identification number"""
        return self._taxid

    @property
    def name(self) -> str:
        """Name of the taxonomic node"""
        return self._name

    @property
    def rank(self) -> str:
        """Rank of the taxonomic node"""
        return self._rank

    @property
    def parent(self) -> str:
        """Parent node"""
        return self._parent

    @property
    def children(self) -> set:
        """Children nodes"""
        return self._children

    @property
    def node_info(self) -> str:
        """
        Node information
        """
        return f"{self.__repr__()}\n" \
               f"type: {self.__class__.__name__}\n" \
               f"taxid: {self.taxid}\n" \
               f"name: {self.name}\n" \
               f"rank: {self.rank}\n" \
               f"parent: {self.parent}\n" \
               f"children: {self.children}\n"

    # Setter methods
    @taxid.setter
    def taxid(self, taxid: Union[str, int]) -> None:
        self._taxid = str(taxid)

    @name.setter
    def name(self, name: str) -> None:
        self._name = str(name)

    @rank.setter
    def rank(self, rank: str) -> None:
        self._rank = str(rank)

    @children.setter
    def children(self, children: set) -> None:
        self._children = set(children)

    @parent.setter
    def parent(self, parent: Node) -> None:
        """Set parent node and update children attribute of parent node"""
        # root node has circular reference to self.
        if parent and parent.taxid != self.taxid:
            assert isinstance(parent, _BaseNode)
            self._parent = parent
            self._updateParent()
        else:
            self._parent = None

    def isAncestorOf(self, node: Node) -> bool:
        """
        Test if the object is an ancestor of another Node.

        Parameters
        ----------
        node:
            Putative descendant node

        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> node.isAncestorOf(root)
        False
        root.isAncestorOf(node)
        True
        """
        if not node.parent or node.parent.taxid == node.taxid:
            return False
        elif node.parent.taxid == self.taxid:
            return True
        else:
            return self.isAncestorOf(node.parent)

    def isDescendantOf(self, node: Node) -> bool:
        """
        Test if the object is an ancestor of another Node.

        Parameters
        ----------
        node:
            Putative ancestor node

        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> node.isDescendantOf(root)
        True
        root.isDescendantOf(node)
        False
        """
        if not self.parent or self.parent.taxid == self.taxid:
            return False
        elif self.parent.taxid == node.taxid:
            return True
        else:
            return self.parent.isDescendantOf(node)

    def _updateParent(self) -> None:
        """
        Add self to parent's children list
        """
        if self._parent:
            self._parent.children.add(self)

    def _relink(self) -> None:
        """
        Bypass self by relinking children to parents
        """
        if not self.parent:
            raise TypeError("Cannot relink a root Node")

        children = self.children

        for child in children:
            child.parent = self.parent
            # Will auto update the parent node

        self.parent.children.discard(self)

    def _to_dict(self):
        """
        Create a dict of self with information to recreate the object.
        """
        dic = dict(self.__dict__)
        if self.parent:
            dic['_parent'] = dic['_parent'].taxid
        dic['type'] = self.__class__.__name__
        del dic['_children']
        return dic


class Node(_BaseNode):
    """
    Taxonomic Node

    Create a Node object contining taxonomic information
    as well as a link to parent and children nodes.

    Parameters
    ---------
    taxid: str or int
        Taxonomic identification number
    name: str, optional
        Node name
    rank: str, optional
        Node rank
    parent: _BaseNode, optional
        The parent Node object

    Notes
    -----
    The `children` property will be dynamically populated when children Nodes
    declare a Node as parent.

    Attributes
    ----------
    taxid
    name
    rank
    children
    parent
    node_info

    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> child = Node(2, "child", "child_rank", root)

    >>> child.taxid
    '2'
    >>> child.rank
    'child_rank'
    >>> child.name
    'child'

    >>> child.parent
    Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None

    >>> root.children
    [Node object:
            Taxid: 2
            Name: child
            Rank: child_rank
            Parent: 1]
    """

    def __init__(self,
                 taxid: Union[str, int],
                 name: Optional[str] = None,
                 rank: Optional[str] = None,
                 parent: Optional[_BaseNode] = None) -> None:
        super().__init__(taxid, name, rank, parent)

    # Property methods
    @property
    def taxid(self) -> str:
        """Taxonomic identification number"""
        return super().taxid

    @property
    def name(self) -> str:
        """Name of the taxonomic node"""
        return super().name

    @property
    def rank(self) -> str:
        """Rank of the taxonomic node"""
        return super().rank

    @property
    def parent(self) -> str:
        """Parent node"""
        return super().parent

    @property
    def children(self) -> list:
        """Children nodes"""
        return super().children

    @property
    def node_info(self) -> str:
        """
        Node information
        """
        return super().node_info

    # Setter methods
    @taxid.setter
    def taxid(self, taxid: Union[str, int]) -> None:
        super(Node, self.__class__).taxid.fset(self, taxid)

    @name.setter
    def name(self, name: str) -> None:
        super(Node, self.__class__).name.fset(self, name)

    @rank.setter
    def rank(self, rank: str) -> None:
        super(Node, self.__class__).rank.fset(self, rank)

    @children.setter
    def children(self, children: list) -> None:
        super(Node, self.__class__).children.fset(self, children)

    @parent.setter
    def parent(self, parent: Node) -> None:
        """Set parent node and update children attribute of parent node"""
        super(Node, self.__class__).parent.fset(self, parent)


class DummyNode(_BaseNode):
    """
    A placeholder for a non-existing Node.

    Will be assigned a random hash id in place of a taxid
    upon creation. Can be inserted between two existing nodes.

    Parameters
    ---------
    taxid: int or str, optional
        Taxonomic identification number
    name: str, optional
        Node name
    rank: str, optional
        Node rank
    parent: _BaseNode, optional
        The parent Node object

    Attributes
    ----------
    taxid
    name
    rank
    children
    parent
    node_info
    """
    def __init__(self,
                 taxid: Optional[Union[str, int]] = None,
                 name: Optional[str] = None,
                 rank: Optional[str] = None,
                 parent: Optional[_BaseNode] = None) -> None:
        if not taxid:
            taxid = _rand_id() # generating random taxid
        super().__init__(taxid, name, rank, parent)

    def insertNode(self, parent: _BaseNode, child: _BaseNode) -> None:
        """
        Insert the dummy node between parent and child

        Parameters
        ----------
        parent: _BaseNode
            Upstream node
        child: _BaseNode
            Downstream node

        Returns
        ------
        None
        """
        child.parent = self
        parent.children.remove(child)
        self.parent = parent

    # Property methods
    @property
    def taxid(self) -> str:
        """Taxonomic identification number"""
        return super().taxid

    @property
    def name(self) -> str:
        """Name of the taxonomic node"""
        return super().name

    @property
    def rank(self) -> str:
        """Rank of the taxonomic node"""
        return super().rank

    @property
    def parent(self) -> str:
        """Parent node"""
        return super().parent

    @property
    def children(self) -> list:
        """Children nodes"""
        return super().children

    @property
    def node_info(self) -> str:
        """Node information"""
        return super().node_info

    # Setter methods
    @taxid.setter
    def taxid(self, taxid: Union[str, int]) -> None:
        super(DummyNode, self.__class__).taxid.fset(self, taxid)

    @name.setter
    def name(self, name: str) -> None:
        super(DummyNode, self.__class__).name.fset(self, name)

    @rank.setter
    def rank(self, rank: str) -> None:
        super(DummyNode, self.__class__).rank.fset(self, rank)

    @children.setter
    def children(self, children: list) -> None:
        super(DummyNode, self.__class__).children.fset(self, children)

    @parent.setter
    def parent(self, parent: Node) -> None:
        """Set parent node and update children attribute of parent node"""
        super(DummyNode, self.__class__).parent.fset(self, parent)


class MergedNode:
    """
    Simple class linking to an instance of (a subclass of) _BaseNode

    Represents a taxonomic node that has been merged with another node and is therefore not
    part of the taxonomy anymore.
    This is not a subclass of _BaseNode.

    Parameters
    ---------
    taxid: int or str
        Taxonomic identification number
    new_node: int or str
        Taxid of node this node has been merged with
    *args: optional
        ignored
    **kwargs: optional
        ignored

    Attributes
    ----------
    taxid
    new_node

    Note
    ----
    `new_node` is provided as a taxid and not as an instance of a Node class.
    An Error will be raised upon trying to access a MergedNode from Taxonomy object if it is linked to a non-existing Node.
    """
    def __init__(self, taxid: Union[str, int], new_node: Union[str, int], *args, **kwargs) -> None:
        self._taxid = str(taxid)
        self._new_node = str(new_node)

    @property
    def taxid(self) -> str:
        """Taxonomic identification number"""
        return self._taxid

    @property
    def new_node(self) -> str:
        """Node this node has been merged with"""
        return self._new_node

    @taxid.setter
    def taxid(self, taxid: Union[str, int]) -> None:
        self._taxid = str(taxid)

    @new_node.setter
    def new_node(self, new_node: Union[str, int]) -> None:
        self._new_node = str(new_node)
