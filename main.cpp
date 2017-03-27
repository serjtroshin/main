//
// by Sergey Troshin, 27 March 2017.
// With thankfulness to https://youtu.be/UaLIHuR1t8Q
// But if smb would watch it
// in DELETION video in case 5 parent can be both red and black, not just black.﻿
//



#include <iostream>
#include <vector>
#include <set>


namespace mystd {
    template <typename T>
    class set {
     private:
        enum color {
            RED,
            BLACK
        };
        struct node {
            T val;
            color cl = RED;
            node * lch = nullptr;
            node * rch = nullptr;
            node * parent = nullptr;
            bool is_root() {
                return parent == nullptr;
            }
            node() {cl = RED;}
            node(const T& val, color cl) : val(val), cl(cl) {}
            node(const T& val, color cl, node* parent) : val(val), cl(cl), parent(parent) {}
            node(T&& val, color cl) : val(val), cl(cl) {}
            node(T&& val, color cl, node* parent) : val(val), cl(cl), parent(parent) {}
            ~node() {
                if (lch != nullptr) {
                    delete lch;
                }
                if (rch != nullptr) {
                    delete rch;
                }
            }
        };
     public:
        class iterator;
        node * root = nullptr;
        node * sibling(node * me) {
            if (me == nullptr || me->is_root()) return nullptr;
            node * a = me->parent->lch;
            node * b = me->parent->rch;
            return (a == me ? b : a);
        }
        bool is_sibling_red(node * me) { // case 1
            node * sib = sibling(me);
            if (sib == nullptr) return 0;
            return sib->cl == RED;
        }
        /**********************************************************************************
         *  if we find that we are red and our parent is red -                            *
         *  we should make some rotation in some cases                                    *
         *  rotate(cur) basically suppose that cur is red and cur's parent is red         *
         **********************************************************************************/
        void right_rotate(node * me, bool change_color) { // we are left child, so rotate our parent on positive angel
            if (me->parent == root)
                root = me;
            node * parent = me->parent;
            me->parent = parent->parent;
            if (parent->parent != nullptr) {
                if (parent->parent->lch == parent)
                    parent->parent->lch = me;
                else
                    parent->parent->rch = me;
            }
            parent->lch = me->rch;
            if (me->rch != nullptr)
                me->rch->parent = parent;
            me->rch = parent;
            parent->parent = me;
            if (change_color) {
                parent->cl = RED;
                me->cl = BLACK;
            }
        }
        // same
        void left_rotate(node * me, bool change_color) { // we are right child
            if (me->parent == root)
                root = me;
            node * parent = me->parent;
            me->parent = parent->parent; // me-to-grdad
            if (parent->parent != nullptr) {
                if (parent->parent->lch == parent)
                    parent->parent->lch = me; //grdad-to-me
                else
                    parent->parent->rch = me;
            }
            parent->rch = me->lch;
            if (me->lch != nullptr)
                me->lch->parent = parent;
            me->lch = parent;
            parent->parent = me;
            if (change_color) {
                parent->cl = RED;
                me->cl = BLACK;
            }
        }
        //DEBUG ONLY
        // calculate max black sum in subtree recursively
        size_t black_sum(node * cur) {
            if (cur == nullptr)
                return 1;
            size_t ans = std::max(black_sum(cur->lch), black_sum(cur->rch));
            if (cur->cl == BLACK)
                ans++;
            return ans;
        }
        //DEBUG ONLY
        // check red-black invariant recursively
        bool is_tree_red_black(node * cur) {
            if (cur == nullptr)
                return 1;
            if (root->cl == RED)
                return 0;
            // red-red relationship
            if (get_color(cur) == RED && (get_color(cur->lch) == RED || get_color(cur->rch) == RED))
                return 0;
            return (black_sum(cur->lch) == black_sum(cur->rch)
                    && is_tree_red_black(cur->lch) && is_tree_red_black(cur->rch));
        }
         /********************************************************
          *        main function that repair invariant           *
          * it's fast and do constant number of rotations at all *
          ********************************************************/
        void check(node * cur) {
            if (cur->parent == nullptr || cur->parent->cl == BLACK) {
                return;
            }
            if (cur->parent->parent == nullptr) {
                cur->parent->cl = BLACK;
                return;
            }
            // so we are red, and our parent too
            if (is_sibling_red(cur->parent)) {
                node * sib = sibling(cur->parent);
                cur->parent->cl = BLACK;
                sib->cl = BLACK;
                node * grand_dad = cur->parent->parent;
                if (!grand_dad->is_root()) {
                    grand_dad->cl = RED;
                    cur = grand_dad;
                    check(cur);
                } else {
                    return;
                }
            } else {
                // now we face 4 cases
                // LR means that we cur(red) is Left child and cur's parent(red too) is Right child
                if (cur->parent->parent->lch == cur->parent && cur->parent->rch == cur) { // LR
                    left_rotate(cur, 0);
                    cur = cur->lch;
                } else if (cur->parent->parent->rch == cur->parent && cur->parent->lch == cur) {// RL
                    right_rotate(cur, 0);
                    cur = cur->rch;
                }
                // only LL or RR ve have now. There we go.
                if (cur->parent->parent->lch == cur->parent && cur->parent->lch == cur) { // LL
                    right_rotate(cur->parent, 1);
                } else if (cur->parent->parent->rch == cur->parent && cur->parent->rch == cur) { // RR
                        left_rotate(cur->parent, 1);
                } else {
                    throw std::invalid_argument("Undefined behaviour");
                }
            }
        }
        /****************************************
         *              INSERTION               *
         ****************************************/
        void insert(T elem) {
            node * new_node = new node(elem, RED);
            if (root == nullptr) {
                root = new_node;
                root->cl = BLACK;
                return;
            }
            node * curr = root;
            /****************************************
             *     find a place to insert binary    *
             ****************************************/
            while (1) {
                if (new_node->val == curr->val) {
                    delete new_node;
                    return;
                }
                if (new_node->val < curr->val) { // идем либо влево, либо вправо
                    if (curr->lch == nullptr) {
                        curr->lch = new_node;
                        new_node->parent = curr;
                        break;
                    } else {
                        curr = curr->lch;
                    }
                } else {
                    if (curr->rch == nullptr) {
                        curr->rch = new_node;
                        new_node->parent = curr;
                        break;
                    } else {
                        curr = curr->rch;
                    }
                }
            }
            /****************************************
             * then trying to repair tree invariant *
             ****************************************/
            // check if all is okey - parent is black
            node * cur = new_node;
            check(cur);
            root->cl = BLACK;
        }
        size_t cnt_h(node * cur) {
            if (cur == nullptr)
                return 0;
            return std::max(cnt_h(cur->lch), cnt_h(cur->rch)) + 1;
        }
        /********************************
         *            PRINT             *
         ********************************/
        void print(node * cur, bool ind = 0) {
            if (cur == nullptr)
                return;
            if (!ind)
                std::cout << "\n---OUTPUT---\n";
            std::cout << "col = " << (cur->cl == BLACK ? "black" : "red") <<
                      ", val = " << cur->val << "| [" << (cur->lch == nullptr ? -1 : cur->lch->val) <<
                      "," << (cur->rch == nullptr ? -1 : cur->rch->val) <<
                      "] parent = " << (cur->parent == nullptr ? -1 : cur->parent->val) << '\n';
            print(cur->lch, 1);
            print(cur->rch, 1);
        }
        ~set() {
            if (root != nullptr) {
                delete root;
            }
        }
        bool empty() {
            return root == nullptr;
        }
        node * find(node * cur, T& val) {
            // if not found - return nullptr
            // else return pointer on node with val
            if (cur == nullptr)
                return nullptr;
            if (cur->val == val) {
                return cur;
            } else if (cur->val < val) {
                return find(cur->rch, val);
            } else {
                return find(cur->lch, val);
            }
        }
        node * last() {
            node * r = root;
            if (r == nullptr)
                return r;
            // find last element for end iterator
            while (r->rch != nullptr)
                r = r->rch;
            return r;
        }
        iterator find(T& val) {
            node * elem = find(root, val);
            return elem == nullptr ? end() : iterator(elem, last());
        }
        node * child_to_delete(node * cur, bool is_left=0) {
            // move 1 right and while can left
            if (!is_left) {
                if (cur->rch != nullptr)
                    return child_to_delete(cur->rch, 1);
                else
                    return cur;
            } else {
                if (cur->lch == nullptr)
                    return cur;
                else
                    return child_to_delete(cur->lch, 1);
            }
        }
        void erase(T val) {
            // if element exist remove it
            node * elem = find(root, val);
            if (elem == nullptr)
                return;
            node * me = child_to_delete(elem); // this node will be deleted implicitly
            // copy value from the node which is about to be deleted...
            // ...to the node which keep the val to be deleted
            elem->val = me->val;
            delete_node(me);
        }
        color get_color(node * n) {
            if (n == nullptr)
                return BLACK;
            else return n->cl;
        }
        void set_color(node * n, color c) {
            if (n == nullptr)
                return;
            else
                n->cl = c;
        }
        bool is_left_child(node * sib) {
            if (sib->parent == nullptr)
                return 0;
            return sib->parent->lch == sib;
        }
        /*******************************
         *   main is DELETE-function   *
         *******************************/
        void delete_node(node * me) {
            node * to_delete = me;
            // if me is root
            // * - means terminal state
            if (me->parent == nullptr) {
                if (me->lch != nullptr) {
                    root = me->lch;
                    root->parent = nullptr;
                    delete me; // we can have only one left right right child
                } else if (me->rch != nullptr) {
                    root = me->rch;
                    root->parent = nullptr;
                    delete me;
                } else {
                    root = nullptr;
                }
                return; // *
            }
            // if me is red node
            if (me->cl == RED) {
                // make me null double-black node
                if (is_left_child(me))
                    me->parent->lch = nullptr;
                else
                    me->parent->rch = nullptr;
                delete to_delete;
                return ; // *
            }
            // if me has red child
            if (get_color(me->lch) == RED || get_color(me->rch) == RED) {
                node * cop = nullptr;
                if (get_color(me->lch) == RED) {
                    cop = me->lch;
                } else {
                    cop = me->rch;
                }
                if (me->parent->rch == me) { // can delete me immediately
                    me->parent->rch = cop;
                } else {
                    me->parent->lch = cop;
                }
                cop->parent = me->parent;
                // make me null double-black node
                if (is_left_child(to_delete))
                    to_delete->parent->lch = nullptr;
                else
                    to_delete->parent->rch = nullptr;
                delete to_delete;
                return;
            }
            // if both children are black (it mean that they are null moreover)
            // if we push the problem - we must solve it another time;
            LOOP:;
            // final state
            if (me->parent == nullptr) {
                if (is_left_child(to_delete))
                    to_delete->parent->lch = nullptr;
                else
                    to_delete->parent->rch = nullptr;
                delete to_delete;
                return;
            }

            // case 1
            // if our sibling is red, but parent is BLACK! - fix it and make some rotation
            node * sib = sibling(me);
            if (is_sibling_red(me) && get_color(me->parent) == BLACK && get_color(sib->lch) == BLACK && get_color(sib->rch) == BLACK) {
                if (is_left_child(me)) {
                    left_rotate(sib, 1);
                } else {
                    throw std::invalid_argument("Undefined behaviour");
                }
            }

            //case 2
            // if node's sibling is black and both sibling's children are black
            // push double-black node up
            sib = sibling(me);
            if (get_color(me->parent) == BLACK && get_color(sib) == BLACK && get_color(sib->lch) == BLACK && get_color(sib->rch) == BLACK) {
                // then we make pushing: sibling gonna be red, parent gonna be double red, me gonna be black
                set_color(me, BLACK);
                set_color(sib, RED);
                set_color(me->parent, BLACK);
                me = me->parent;
                goto LOOP;
            }

            // case 3 - final state when our sibling and it's children are black but me's parent is red
            if (!is_sibling_red(me) && get_color(me->parent) == RED && get_color(sib->lch) == BLACK && get_color(sib->rch) == BLACK) {
                sib = sibling(me);
                set_color(sib, RED);
                set_color(me, BLACK);
                set_color(me->parent, BLACK);
                if (is_left_child(to_delete))
                    to_delete->parent->lch = nullptr;
                else
                    to_delete->parent->rch = nullptr;
                delete to_delete;
                return;
            }

            //case 4
            // if me is lch, and me's black sibling has left-red and right-black child
            // we make right rotation from left-red child
            // simmetric case if we are right child
            sib = sibling(me);
            if (get_color(sib) == BLACK) {
                if (is_left_child(me) && get_color(sib->lch) == RED && get_color(sib->rch) == BLACK){ // usual case
                    right_rotate(sib->lch, 1);
                } else if (!is_left_child(me) && get_color(sib->rch) == RED && get_color(sib->lch) == BLACK){ // simmetric
                    left_rotate(sib->rch, 1);
                }
            }

            // case 5
            // if me is left child, me's sibling is black, sibling's  right child is red;
            // simmetric if me is right child
            sib = sibling(me);
            if (get_color(sib) == BLACK) {
                if (is_left_child(me) && get_color(sib->rch) == RED){ // usual case
                    left_rotate(sib, 0);
                    set_color(sib, me->parent->cl);
                    set_color(me->parent, BLACK);
                    set_color(sib->rch, BLACK);
                } else if (!is_left_child(me) && get_color(sib->lch) == RED){ // simmetric
                    right_rotate(sib, 0);
                    set_color(sib, me->parent->cl);
                    set_color(me->parent, BLACK);
                    set_color(sib->lch, BLACK);
                }
                // make me null double-black node
                if (is_left_child(to_delete))
                    to_delete->parent->lch = nullptr;
                else
                    to_delete->parent->rch = nullptr;
                delete to_delete;
                return;
                // *
            }
            goto LOOP;
            return;
        }
        class iterator {
            node * ptr;
         public:
            // is_end using for end iterator
            bool is_end = false;
            node * last;
            iterator(node * ptr, node * last) : ptr(ptr), last(last) {}
            node * next(node * p, node * prev = nullptr) {
                if (ptr == last)
                    is_end = 1;
                if (is_end)
                    return nullptr;
                if (p->rch != nullptr && p->rch != prev) {
                    p = p->rch;
                    return p;
                }
                if (p->parent != nullptr) {
                    return next(p->parent, p);
                }
                return nullptr;
            }
            node * prev(node * p, node * prev = nullptr) {
                if (is_end) {
                    is_end = 0;
                    return last;
                }
                if (p->lch != nullptr && p->lch != prev) {
                    p = p->lch;
                    return p;
                }
                if (p->parent != nullptr) {
                    return next(p->parent, p);
                }
                return nullptr;
            }
            iterator& operator ++ (int) {
                ptr = next(ptr);
                return (*this);
            }
            iterator operator ++ () {
                auto it = *this;
                ptr = next(ptr);
                return it;
            }
            iterator& operator -- (int) {
                ptr = prev(ptr);
                return (*this);
            }
            iterator operator -- () {
                auto it = *this;
                ptr = prev(ptr);
                return it;
            }
            node* operator -> () {
                return ptr;
            }
            node* operator -> () const {
                return ptr;
            }
            T& operator * () {
                return ptr->val;
            }
            T& operator * () const {
                return ptr->val;
            }
            bool operator == (const iterator& other) const {
                return ptr == other.ptr;
            }
            bool operator != (const iterator& other) const {
                return ptr != other.ptr;
            }
            bool null() {
                return ptr == nullptr;
            }
        };
        iterator begin() {
            iterator it(root, last());
            // find mostly left node - it'll be begin
            while(it->lch != nullptr)
                it--;
            return it;
        }
        iterator end() {
            iterator it(nullptr, last());
            it.is_end = 1;
            while(!it.null() && it->lch != nullptr)
                it++;
            return it;
        }
    };
}
int main() {
    mystd::set<int> st;
    std::set<int> s;
    int a;
    int i = 0, n = 2000000;
    while (i++ < n) {
        a = rand() % n;
        //std::cout << a << ' ';
        st.insert(a);
    }
    while (!st.empty()) {
        //st.print(st.root);
        st.erase(*st.begin());
    }
    return 0;
}