#if (SILVERLIGHT)
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;

namespace FarseerGames.FarseerPhysics.Collections.Generic
{
    public class LinkedList<T>
    {
        private LinkedListNode<T> _first = null;
        private LinkedListNode<T> _last = null;

        public int Length
        {
            get
            {
                int i = 0;
                LinkedListNode<T> n = _first;
                while (n != null)
                {
                    n = n.Next;
                    i++;
                }
                return i;
            }
        }

        public LinkedListNode<T> First
        {
            get
            {
                return _first;
            }
        }

        public void AddLast(LinkedListNode<T> node)
        {
            if (_last != null)
            {
                _last.Next = node;
            }
            if (_first == null)
            {
                _first = node;
            }
            node.Previous = _last;
            node.Next = null;
            _last = node;
        }

        public void Remove(LinkedListNode<T> node)
        {
            if (node.Next != null)
            {
                node.Next.Previous = node.Previous;
            }
            else
            {
                _last = node.Previous;
            }
            if (node.Previous != null)
            {
                node.Previous.Next = node.Next;
            }
            else
            {
                _first = node.Next;
            }
            node.Next = null;
            node.Previous = null;
        }
    }
}
#endif