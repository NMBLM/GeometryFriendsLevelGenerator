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
    public class LinkedListNode<T>
    {
        private T _value = default(T);
        private LinkedListNode<T> _next = null;
        private LinkedListNode<T> _previous = null;

        public LinkedListNode(T value)
        {
            _value = value;
        }

        public LinkedListNode<T> Next
        {
            get
            {
                return _next;
            }
            internal set
            {
                _next = value;
            }
        }

        public LinkedListNode<T> Previous
        {
            get
            {
                return _previous;
            }
            internal set
            {
                _previous = value;
            }
        }

        public T Value
        {
            get
            {
                return _value;
            }
        }

    }
}
#endif