using System;
using System.Collections.Generic;
using System.Drawing;
using UnityEngine;

namespace GeometryFriends.LevelGenerator
{
    
    //Playable Area: top left corner X=40 and Y=40  bottom right corner X=1240, Y=760
    
    public enum BlockType : byte
    {
        Unreachable = 0,
        Platform = 1,
        CirclePlatform = 2,    //Is a platform that only blocks the Circle
        RectanglePlatform = 3, //Is a platform that only blocks the Rectangle
        RectangleCanReach = 4,
        CircleCanReach = 5,
        BothCanReach = 6,
        CooperativeCanReach = 7,
        RectangleCanReachCirclePlatform = 8,
        CircleCanReachRectanglePlatform = 9,         //Is a Rectangle Platform that the Circle can Reach
        CooperativeCanReachRectanglePlatform = 10,    //Is a Rectangle Platform that the Circle can Reach when using cooperation to jump
    }

    enum RecReachState : byte
    {
        Spawning,
        SpawnFalling,
        Falling,
        Platform,
        GoRight,
        GoLeft,
        JumpRight,
        JumpLeft,
        FoundHoleRight,
        FoundHoleLeft,
        DeadEnd
    }
    
    
    public class ReachabilityFitness : FitnessCalculator
    {
        public float blockSize;
        public BlockType[,] grid;
        public int xGridLen, yGridLen;
        
        public int circleLen;

        public int rectangleStartLen, rectangleMinLen, rectangleMaxLen;
        //Common Factors for 1200 and 720 are The common factors are:
        //blockSize:   1,  2,  3,  4,  5,  6,  8, 10, 12, 15, 16, 20, 24, 30, 40, 48, 60, 80,120,240
        //xGridLen: 1200,600,400,300,240,200,150,120,100, 80, 75, 60, 50, 40, 30, 25, 20, 15, 10,  5
        //yGridLen: 720 ,360,240,180,144,120, 90, 72, 60, 48, 45, 36, 30, 24, 18, 15, 12,  9,  6,  3
        
        //Circle takes 80x80
        //Rectangle takes 100x100 min/max 50x200 or 200x50.
        //NumOfBlocks for Circle:
        // 80, 40,-,20,16,-,10, 8,-,-,5, 4,-,-,2,-,-,1,-,-
        //NumOfBlocks for Rectangle: 
        //100, 50,-,25,20,-, -,10,-,-,-, 5,-,-,-,-,-,-,-,-
        // 50, 25,-, -,10,-, -, 5,-,-,-, -,-,-,-,-,-,-,-,-
        //200,100,-,50,40,-,25,20,-,-,-,10,-,-,5,-,-,-,-,-
        
        public ReachabilityFitness( float blockSize = 20f)
        {
            //For now fix in BlockSize in 20 so 60x, 36y
            //Circe is 4x4
            //Rectangle is 5x5 or 2.5x10 or 10x2.5
            this.blockSize = blockSize;
            // + 2 because always one line of platforms all around
            xGridLen = (int) ((1240 - 40) / blockSize + 0.5f) +2; // +0.5f to round up;
            yGridLen = (int) ((760 - 40) / blockSize + 0.5f) +2; // +0.5f to round up;

            circleLen = (int) (80 / blockSize + 0.5f);
            rectangleStartLen = (int) (100 / blockSize + 0.5f);
            rectangleMinLen = (int) (50 / blockSize +0.5f); 
            rectangleMaxLen = (int) (200 / blockSize + 0.5f);
            
            /** /
            Debug.Log("xGridLen: " + xGridLen + " yGridLen: " + yGridLen);
            Debug.Log("circleLen: " + circleLen);
            Debug.Log("rectangleStartLen: "+ rectangleStartLen + " rectangleMinLen: " + rectangleMinLen + " rectangleMaxLen: " + rectangleMaxLen);
            /**/
            
            grid = new BlockType[xGridLen,yGridLen]; 
        }
        public override float CalculateFitness(LevelDNA level)
        {
            InitGrid(level);
            //RectangleReachability(level);
            RectangleReachabilityStates(level);
            CircleReachability(level);
            return 0;
        }

        public void InitGrid(LevelDNA level)
        {
            foreach (var plat in level.platforms)
            {
                int platPosX = (int) ((plat.position.X - 40) / this.blockSize)  + 1;
                int platPosY = (int) ((plat.position.Y - 40)/ this.blockSize)  + 1;
                int platWidth = (int) (plat.width / this.blockSize + 0.5f);
                int platHeight = (int) (plat.height / this.blockSize + 0.5f);
                
                if (platPosX > xGridLen || platPosY > yGridLen)
                {
                    Debug.Log("Bad platform positioning (" + plat.position.X + " , " + plat.position.Y+ ")");
                }
                for (int i = platPosX; i < (platPosX + platWidth) && i < xGridLen; i++)
                {
                    for (int j = platPosY; j < (platPosY + platHeight) && j < yGridLen; j++)
                    {
                        switch (plat.platformType)
                        {
                            case PlatformType.Common:
                                grid[i, j] = BlockType.Platform;
                                break;
                            case PlatformType.CirclePlatform:
                                grid[i, j] = BlockType.CirclePlatform;
                                break;
                            case PlatformType.RectanglePlatform:
                                grid[i, j] = BlockType.RectanglePlatform;
                                break;
                        }
                    }
                    
                }
            }

            for (int i = 0; i < yGridLen; i++)
            {
                grid[0,i] = BlockType.Platform;
                grid[xGridLen-1,i] = BlockType.Platform;
            }

            for (int i = 0; i < xGridLen; i++)
            {
                grid[i,0] = BlockType.Platform;
                grid[i,yGridLen-1] = BlockType.Platform;
            }
            
        }
        public void RectangleReachability(LevelDNA level)
        {
            int x = (int) ((level.rectangleSpawn.position.X - 40) / this.blockSize) + 1;
            int y = (int) ((level.rectangleSpawn.position.Y - 40) / this.blockSize) + 1;
            List<Tuple<Point,int>> list = new List<Tuple<Point,int>>();
            list.Add(new Tuple<Point,int>(new Point(x, y),0));
            while (list.Count > 0)
            {
                var startPos = list[0];
                x = startPos.Item1.X;
                y = startPos.Item1.Y;
                var dir = startPos.Item2;
                list.RemoveAt(0);
                
                while (RectangleVisit(x, y))
                {
                    for (int i = 0; i < rectangleStartLen && x+i < xGridLen; i++)
                    {
                        RectangleVisit(x+i, y);
                    }
                    y += 1;
                }

                if (y >= yGridLen || grid[x, y] == BlockType.Platform)
                {
                    y -= 1;
                    //list.Add(new Tuple<Point,int>(new Point(x, y),-1));
                    //list.Add(new Tuple<Point,int>(new Point(x, y),+1));
                }

            }
            
        }

   
        public void CircleReachability(LevelDNA level)
        {
            int x = (int) ((level.circleSpawn.position.X - 40)/ this.blockSize) + 1;
            int y = (int) ((level.circleSpawn.position.Y - 40)/ this.blockSize) + 1;
            List<Tuple<Point,int>> list = new List<Tuple<Point,int>>();
            list.Add(new Tuple<Point,int>(new Point(x, y),0));
            while (list.Count > 0)
            {
                var startPos = list[0];
                x = startPos.Item1.X;
                y = startPos.Item1.Y;
                var dir = startPos.Item2;
                list.RemoveAt(0);
                
                while (CircleVisit(x, y))
                {
                    for (int i = 0; i < circleLen && x+i < xGridLen; i++)
                    {
                        CircleVisit(x+i, y);
                    }
                    y += 1;
                }

                if (y >= yGridLen || grid[x, y] == BlockType.Platform)
                {
                    y -= 1;
                    //list.Add(new Tuple<Point,int>(new Point(x, y),-1));
                    //list.Add(new Tuple<Point,int>(new Point(x, y),+1));
                }

            }
        }
        
        private bool CircleVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return false;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    grid[x, y] = BlockType.CircleCanReach;
                    return true;
                case BlockType.Platform:
                    return false;
                case BlockType.CirclePlatform:
                    return false;
                case BlockType.RectanglePlatform:
                    grid[x, y] = BlockType.CircleCanReachRectanglePlatform;
                    return true;
                case BlockType.CircleCanReach:
                    return true;
                case BlockType.RectangleCanReach:
                    grid[x, y] = BlockType.BothCanReach;
                    return true;
                case BlockType.BothCanReach:
                    return true;
                case BlockType.CooperativeCanReach:
                    grid[x, y] = BlockType.CircleCanReach;
                    return true;
                case BlockType.RectangleCanReachCirclePlatform:
                    return false;
                case BlockType.CircleCanReachRectanglePlatform:
                    return true;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    grid[x, y] = BlockType.CircleCanReachRectanglePlatform;
                    return true;
                default:
                    return false;
            }
        }
        
        public void CoopReachability(LevelDNA level)
        {
            int startPosX = (int) ((level.circleSpawn.position.X - 40)/ this.blockSize);
            int startPosY = (int) ((level.circleSpawn.position.Y - 40)/ this.blockSize);

        }
        private bool CoopVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return false;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    grid[x, y] = BlockType.CooperativeCanReachRectanglePlatform;
                    return true;
                case BlockType.Platform:
                    return false;
                case BlockType.CirclePlatform:
                    return false;
                case BlockType.RectanglePlatform:
                    grid[x, y] = BlockType.CooperativeCanReachRectanglePlatform;
                    return true;
                case BlockType.CircleCanReach:
                    return true;
                case BlockType.RectangleCanReach:
                    grid[x, y] = BlockType.BothCanReach;
                    return true;
                case BlockType.BothCanReach:
                    return true;
                case BlockType.CooperativeCanReach:
                    return true;
                case BlockType.RectangleCanReachCirclePlatform:
                    return false;
                case BlockType.CircleCanReachRectanglePlatform:
                    return true;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    return true;
                default:
                    return false;
            }
        }


        public void RectangleReachabilityStates(LevelDNA level)
        {
            int x = (int) ((level.rectangleSpawn.position.X - 40) / this.blockSize) + 1;
            int y = (int) ((level.rectangleSpawn.position.Y - 40) / this.blockSize) + 1;
            List<Tuple<Point,RecReachState>> stateList = new List<Tuple<Point,RecReachState>>();
            var state = RecReachState.Spawning;
            
            stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),state));
            
            while (stateList.Count > 0)
            {
                x = stateList[0].Item1.X;
                y = stateList[0].Item1.Y;
                state = stateList[0].Item2;
                stateList.RemoveAt(0);
                bool haveToStop = false;
                int platformX = x;
                
                switch (state)
                {
                case RecReachState.Spawning:
                    if (!TestSpawning(x,y))
                    {
                        return;
                    };
                    y += rectangleStartLen - 1;
                    state = RecReachState.SpawnFalling;
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),RecReachState.Falling));
                    break;
                case RecReachState.SpawnFalling:
                    haveToStop = false;
                    while (!haveToStop)
                    {
                        for (int i = 0; i < rectangleStartLen && x+i < xGridLen; i++)
                        {
                            if (!RectangleVisit(x + i, y))
                            {
                                haveToStop = true;
                                platformX = x + i;
                                break;
                            };
                        }
                        y += 1;
                    }
                    for (int i = 0; i < rectangleStartLen && x+i < xGridLen; i++)
                    {
                        UndoRectangleVisit(x+i,y);
                    }
                    y -= 1;
                    Debug.Log("added L,R");
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(platformX, y),RecReachState.GoRight));
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(platformX, y),RecReachState.GoLeft));
                    break;
                case RecReachState.Falling:
                    haveToStop = false;
                    while (!haveToStop)
                    {
                        for (int i = 0; i < rectangleMaxLen && x+i < xGridLen; i++)
                        {
                            if (!RectangleVisit(x + i, y))
                            {
                                haveToStop = true;
                                platformX = x + i;
                                break;
                            };
                        }
                        y += 1;
                    }
                    for (int i = 0; i < rectangleMaxLen && x+i < xGridLen; i++)
                    {
                        UndoRectangleVisit(x+i,y);
                    }
                    y -= 1;
                    Debug.Log("added L,R");
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(platformX, y),RecReachState.GoRight));
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(platformX, y),RecReachState.GoLeft));
                    break;
                case RecReachState.Platform:
                    for (int i = 0; i < rectangleStartLen && x+i < xGridLen; i++)
                    {
                        UndoRectangleVisit(x+i,y);
                    }
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),RecReachState.GoRight));
                    stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),RecReachState.GoLeft));
                    break;
                case RecReachState.GoRight:
                    //ExtendRectangle
                    haveToStop = false;
                    y = y - 1;
                    while (!haveToStop)
                    {
                        if (RectangleVisit(x, y + 1)) //check if there is no platform bellow
                        {
                            UndoRectangleVisit(x, y + 1);
                            haveToStop = true;
                            stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),RecReachState.FoundHoleRight));
                            break;
                        }
                        for (int i = 0; i < rectangleMaxLen && y-i >0; i++)
                        {
                          
                            if (!RectangleVisit(x, y-i))
                            {
                                /* Found wall Need to check if can climb
                                if (i == 0)
                                {
                                    Debug.Log("Found Wall");
                                    for (; i < rectangleMinLen; i++)
                                    {
                                        if (RectangleVisit(x, y - i))
                                        {
                                            
                                        }
                                    }
                                }
                                */
                                Debug.Log("Found Plat up");
                                if (i < rectangleMinLen-1)
                                {
                                    Debug.Log("IsBelowMinLen");
                                    haveToStop = true;
                                    for (int j = 0; j < i; j++)
                                    {
                                        UndoRectangleVisit(x,y-j);
                                    }
                                    break;
                                }
                            };
                        }
                        Debug.Log("Checked x: " + x);
                        x += 1;
                    }
                    break;
                case RecReachState.GoLeft:
                    haveToStop = false;
                    y = y - 1;
                    while (!haveToStop)
                    {
                        if (RectangleVisit(x, y + 1)) //check if there is a platform below
                        {
                            UndoRectangleVisit(x, y + 1);
                            haveToStop = true;
                            stateList.Add(new Tuple<Point, RecReachState>(new Point(x, y),RecReachState.FoundHoleLeft));
                        }
                        for (int i = 0; i < rectangleMaxLen && y-i >0; i++)
                        {
                            if (!RectangleVisit(x, y-i))
                            {
                                if (i < rectangleMinLen-1)
                                {
                                    haveToStop = true;
                                    for (int j = 0; j < i; j++)
                                    {
                                        UndoRectangleVisit(x,y-j);
                                    }
                                    break;
                                }
                            };
                        }
                        x -= 1;
                    }
                    break;
                case RecReachState.JumpRight:
                    break;
                case RecReachState.JumpLeft:
                    break;
                case RecReachState.FoundHoleRight:
                    //Check if he can fit in the hole
                    y = y - 1;//be at the hole level
                    for (int i = 0; i < rectangleMinLen; i++)
                    {
                        
                    }
                    break;
                case RecReachState.FoundHoleLeft:
                    break;
                case RecReachState.DeadEnd:
                    break;
                }
            }
        }
        //Returns True if Rectangle can reach, False if it is blocked
        private bool RectangleVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return false;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    grid[x, y] = BlockType.RectangleCanReach;
                    return true;
                case BlockType.Platform:
                    return false;
                case BlockType.CirclePlatform:
                    grid[x, y] = BlockType.RectangleCanReachCirclePlatform;
                    return true;
                case BlockType.RectanglePlatform:
                    return false;
                case BlockType.CircleCanReach:
                    grid[x, y] = BlockType.BothCanReach;
                    return true;
                case BlockType.RectangleCanReach:
                    return true;
                case BlockType.BothCanReach:
                    return true;
                case BlockType.CooperativeCanReach:
                    grid[x, y] = BlockType.BothCanReach;
                    return true;
                case BlockType.RectangleCanReachCirclePlatform:
                    return true;
                case BlockType.CircleCanReachRectanglePlatform:
                    return false;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    return false;
                default:
                    return false;
            }
        }
        private bool RectangleCanVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return false;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    return true;
                case BlockType.Platform:
                    return false;
                case BlockType.CirclePlatform:
                    return true;
                case BlockType.RectanglePlatform:
                    return false;
                case BlockType.CircleCanReach:
                    return true;
                case BlockType.RectangleCanReach:
                    return true;
                case BlockType.BothCanReach:
                    return true;
                case BlockType.CooperativeCanReach:
                    return true;
                case BlockType.RectangleCanReachCirclePlatform:
                    return true;
                case BlockType.CircleCanReachRectanglePlatform:
                    return false;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    return false;
                default:
                    return false;
            }
        }
        private void UndoRectangleVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    break;
                case BlockType.Platform:
                    break;
                case BlockType.CirclePlatform:
                    break;
                case BlockType.RectanglePlatform:
                    break;
                case BlockType.CircleCanReach:
                    break;
                case BlockType.RectangleCanReach:
                    grid[x, y] = BlockType.Unreachable;
                    break;
                case BlockType.BothCanReach:
                    grid[x, y] = BlockType.CircleCanReach;
                    break;
                case BlockType.CooperativeCanReach:
                    break;
                case BlockType.RectangleCanReachCirclePlatform:
                    grid[x, y] = BlockType.CirclePlatform;
                    break;
                case BlockType.CircleCanReachRectanglePlatform:
                    break;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    break;
            }
        }

        private void UndoCircleVisit(int x, int y)
        {
            if (x >= xGridLen || y >= yGridLen || x < 0 || y <0)
            {
                return;
            }
            switch (grid[x,y])
            {
                case BlockType.Unreachable:
                    break;
                case BlockType.Platform:
                    break;
                case BlockType.CirclePlatform:
                    break;
                case BlockType.RectanglePlatform:
                    break;
                case BlockType.CircleCanReach:
                    grid[x, y] = BlockType.Unreachable;
                    break;
                case BlockType.RectangleCanReach:
                    break;
                case BlockType.BothCanReach:
                    grid[x, y] = BlockType.RectangleCanReach;
                    break;
                case BlockType.CooperativeCanReach:
                    grid[x, y] = BlockType.Unreachable;
                    break;
                case BlockType.RectangleCanReachCirclePlatform:
                    break;
                case BlockType.CircleCanReachRectanglePlatform:
                    grid[x, y] = BlockType.RectanglePlatform;
                    break;
                case BlockType.CooperativeCanReachRectanglePlatform:
                    grid[x, y] = BlockType.RectanglePlatform;
                    break;
            }
        }
        public bool TestSpawning(int x, int y)
        {
            bool stop = false;
            for (int i = 0; i < rectangleStartLen && y+i < yGridLen && !stop; i++)
            {
                for (int h = 0; h < rectangleStartLen && x+h < xGridLen; h++)
                {
                    if(!RectangleVisit(x+h, y+i))
                    {
                        stop = true;
                        break;
                    };
                } 
            }
            if (stop)
            {
                for (int i = 0; i < rectangleStartLen && y+i < yGridLen; i++)
                {
                    for (int h = 0; h < rectangleStartLen && x+h < xGridLen; h++)
                    {
                        UndoRectangleVisit(x+h,y+i);
                    } 
                }

                return false;
            }
            return true;
        }


    }
}