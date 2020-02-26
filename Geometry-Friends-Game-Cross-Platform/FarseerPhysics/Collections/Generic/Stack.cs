#if (Silverlight)
using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Collections.Generic;

namespace FarseerGames.FarseerPhysics.Collections.Generic
{
    public class Stack<T>
    {
        T[] _data = null;
        int _cur = -1;

        public int Count
        {
            get
            {
                return _cur + 1;
            }
        }

        public Stack()
        {
        }

        public Stack(int size)
        {
            _data = new T[size];
        }

        public virtual void Push(T item)
        {
            _cur++;
            if (_cur == _data.Length)
            {
                if (_cur == 0)
                {
                    _data = new T[8];
                }
                else
                {
                    T [] tmp = new T[_cur * 2];
                    _data.CopyTo(tmp, 0);
                    _data = tmp;
                }
            }
            _data[_cur] = item;
        }

        public T Pop()
        {
            if (_cur < 0)
            {
                throw new InvalidOperationException();
            }
            T item = _data[_cur];
            _cur--;
            return item;
        }
    }
}
#endif